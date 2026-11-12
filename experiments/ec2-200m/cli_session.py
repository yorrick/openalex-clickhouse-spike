"""Use the existing AWS CLI certification role session, without exposing credentials.

CLI role credentials can remain valid after the underlying SSO refresh token has
expired. This is the sole local control-plane credential provider, not an
alternate account or a credential retry chain. Never serialize the Session.
"""
import json,subprocess,boto3

def certification():
 result=subprocess.run(['aws','configure','export-credentials','--profile','certification','--format','process'],capture_output=True,text=True)
 if result.returncode:
  raise RuntimeError('Certification CLI credentials unavailable; renew aws sso login --profile certification')
 c=json.loads(result.stdout)
 session=boto3.Session(aws_access_key_id=c['AccessKeyId'],aws_secret_access_key=c['SecretAccessKey'],aws_session_token=c['SessionToken'],region_name='us-east-1')
 assert session.client('sts').get_caller_identity()['Account']=='502425560524'
 return session
