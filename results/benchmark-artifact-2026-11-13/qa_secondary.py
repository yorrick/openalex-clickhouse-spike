from pathlib import Path
from playwright.sync_api import sync_playwright
import json,hashlib
H=Path(__file__).resolve().parent;P=json.loads((H/'artifact-payload.json').read_text());before=hashlib.sha256((H/'artifact.html').read_bytes()).hexdigest();checks={}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True);page=b.new_page(viewport={'width':1440,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto((H/'artifact.html').as_uri());page.wait_for_function('window.OA')
 # Every legacy arm exposes its actual SQL; these are a distinct experiment from the cohort control.
 for arm,c in P['legacy_tuning'].items():
  page.locator('#tuning button[data-arm="'+arm+'"]').click();texts=page.locator('#tuning pre').all_text_contents();assert c['sql'] in texts,(arm,'Legacy tuning SQL not exact')
 checks['five_legacy_tuning_sql_bodies']=True
 # All tuning-history buttons select the exact recorded profile and case in the main inspector.
 buttons=page.locator('#tuning button[data-profile]').evaluate_all('(xs)=>xs.map(x=>({...x.dataset}))')
 for z in buttons:
  sel='#tuning button[data-profile="'+z['profile']+'"][data-cohort="'+z['cohort']+'"][data-engine="'+z['engine']+'"]';page.locator(sel).click();active=page.evaluate('({cohort:OA.currentRecord().cohort,engine:OA.currentRecord().engine_key,profile:OA.currentRecord().profile_id})');assert active=={'cohort':z['cohort'],'engine':z['engine'],'profile':z['profile']}
 checks['tuning_links_to_exact_profiles']=len(buttons)
 # Focus survives real select changes, including the graph seed selector.
 page.locator('#cohort-select').select_option('200m');page.locator('#cell-q05-clickhouse_ec2').click()
 for sel,val in [('#engine-select','postgres_ec2'),('#seed-select','2003585639'),('#engine-select','clickhouse_ec2')]:
  page.locator(sel).focus();page.locator(sel).select_option(val);assert page.evaluate('document.activeElement.id')==sel[1:]
 checks['engine_profile_seed_focus']=True
 # Historical timings are not assessed as zero target passes.
 for cid in ['2m','10m','32m']:
  page.locator('#cohort-select').select_option(cid);text=page.locator('#family-table-wrap').inner_text().lower();assert 'not assessed' in text
 checks['historical_footer_unassessed']=True
 # The slider is storage arithmetic only, with constant full-dimension baseline.
 slider=page.locator('#proj-slider');attrs=slider.evaluate('(x)=>({min:x.min,max:x.max,step:x.step})')
 for value in [200313862,510372821]:
  slider.evaluate('(x,v)=>{x.value=String(v);x.dispatchEvent(new Event("input",{bubbles:true}))}',value);actual=float(slider.input_value());pred=P['storage']['fixed_dimension_bytes']+P['storage']['variable_bytes_200m']*actual/P['storage']['reference_works'];out=page.locator('#proj-out').inner_text();assert f'{pred/1e9:,.3f}' in out,(value,attrs,actual,out,pred)
 checks['conditional_storage_slider']=True
 # Open schema/view controls and compare each code block to the exact source text.
 page.locator('#dataset details').evaluate_all('(xs)=>xs.forEach(x=>x.open=true)');page.wait_for_timeout(150)
 schema_expected=[P['schemas']['postgres_200m'],'\n'.join(sql+';' for name,sql in P['schemas']['postgres_200m_indexes']),P['schemas']['clickhouse_200m'],P['schemas']['clickhouse_projection'],P['schemas']['legacy_clickhouse']]
 allcode=page.locator('#dataset pre').all_text_contents()
 for sql in schema_expected:assert sql in allcode,('Schema SQL not found exactly',sql[:65])
 page.locator('#node-ath').click()
 athcode=page.locator('#node-detail pre').all_text_contents()
 for view in P['cohorts']['200m'].get('athena_views',[]):assert view['sql'] in athcode,('Athena DDL not exact',view['sql'][:65])
 checks['schema_indexes_projection_and_200m_athena_ddl_exact']=True
 # Wide data tables/code scroll locally even with every data disclosure open.
 for width in [1440,390]:
  page.set_viewport_size({'width':width,'height':1000 if width>500 else 844});assert page.evaluate('document.documentElement.scrollWidth<=document.documentElement.clientWidth+2'),('Expanded dataset overflow',width)
  if width==390:assert all(x=='inline' for x in page.locator('#flow .arrow .v').evaluate_all('(xs)=>xs.map(x=>getComputedStyle(x).display)'))
 checks['mobile_visible_directional_connectors_and_expanded_data_fit']=True
 assert not errors,errors;b.close()
assert hashlib.sha256((H/'artifact.html').read_bytes()).hexdigest()==before
(H/'qa-secondary.json').write_text(json.dumps({'html_sha256':before,'checks':checks,'javascript_errors':errors},indent=2)+'\n');print(json.dumps(checks,indent=2))
