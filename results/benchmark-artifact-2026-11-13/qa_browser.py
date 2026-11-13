from pathlib import Path
from playwright.sync_api import sync_playwright
import json,hashlib,statistics,math
H=Path(__file__).resolve().parent;HTML=H/'artifact.html';expected=json.loads((H/'artifact-payload.json').read_text());before=hashlib.sha256(HTML.read_bytes()).hexdigest()
checked=0;sql_checked=0;viewport_results=[];errors=[]
def no_overflow(page,width,where):
 box=page.evaluate('({width:innerWidth,client:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth,charset:document.characterSet,mode:document.compatMode})')
 assert box['width']==width and box['charset']=='UTF-8' and box['mode']=='CSS1Compat',(where,box)
 assert box['scroll']<=box['client']+2,('page overflow',width,where,box)
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 page=browser.new_page(viewport={'width':1440,'height':1000});page.on('pageerror',lambda e:errors.append(str(e)));page.goto(HTML.as_uri());page.wait_for_function('window.OA && window.OA.currentRecord')
 assert json.loads(page.locator('#payload').text_content())==expected,'Embedded parsed payload differs from immutable source'
 for width in [1440,1000,390]:
  page.set_viewport_size({'width':width,'height':1000 if width>500 else 844})
  for cid in expected['cohorts']:
   page.locator('#cohort-select').select_option(cid)
   cohort_records=[r for r in expected['records'] if r['cohort']==cid]
   selected=[r for r in cohort_records if r['selected']]
   engines=set(r['engine_key'] for r in selected)
   visible=set(page.locator('[id^="cell-q01-"]').evaluate_all('(xs)=>xs.map(x=>x.dataset.engine)'));assert visible==engines,(cid,visible,engines)
   for fam in ['q01','q02','q03','q04','q05','q06','q07']:
    for eng in engines:
     rs=[r for r in selected if r['family']==fam and r['engine_key']==eng];el=page.locator('#cell-'+fam+'-'+eng);val=el.get_attribute('data-value')
     if all(r['state'] in ['complete','historical'] for r in rs):assert abs(float(val)-max(r['median_seconds'] for r in rs))<1e-8,(cid,fam,eng,val)
     else:assert val is None,(cid,fam,eng,'Incomplete case rendered a numeric median',val)
   for r in cohort_records:
    # Exercise real cohort/cell/profile/seed controls rather than only the QA hook.
    page.locator('#cell-'+r['family']+'-'+r['engine_key']).click()
    if r.get('seed'):page.locator('#seed-select').select_option(r['seed'])
    page.locator('#profile-select').focus();page.locator('#profile-select').select_option(r['profile_id']);assert page.evaluate('document.activeElement.id')=='profile-select',('Profile select lost keyboard focus',r['label'])
    active=page.evaluate('({cohort:OA.currentRecord().cohort,engine:OA.currentRecord().engine_key,profile:OA.currentRecord().profile_id,case:OA.currentRecord().case_key})')
    assert active=={'cohort':cid,'engine':r['engine_key'],'profile':r['profile_id'],'case':r['case_key']},(r['label'],active)
    assert page.locator('#ins-state').get_attribute('data-state')==r['state']
    if r.get('sql') is not None:
     actual=page.locator('#sql-body').text_content();assert actual==r['sql'],(cid,r['engine_key'],r['label'],'SQL bytes changed')
     assert hashlib.sha256(actual.encode()).hexdigest()==r['sql_sha256'];assert page.locator('#sql-sha').text_content()==r['sql_sha256'];sql_checked+=1
    else:
     assert 'not recorded' in page.locator('#inspector').inner_text().lower()
     assert page.locator('#copy-sql').count()==0 or not page.locator('#copy-sql').is_enabled()
    if r['state'] not in ['complete','historical']:
     assert 'none' in page.locator('#ins-median').inner_text().lower(),(r['label'],'False median')
    if r['sql_status']=='not_executed':assert 'not executed' in page.locator('#sql-figure').inner_text().lower()
    assert not any(bad in page.locator('#inspector').inner_text() for bad in ['NaN','undefined','[object Object]'])
    no_overflow(page,width,(cid,r['engine_key'],r['label']));checked+=1
    if checked%50==0:print('Checked',checked,'record/viewport interactions',flush=True)
  # Every dataflow node is independently clickable, including repeated source nodes.
  for node in page.locator('#flow button').evaluate_all('(xs)=>xs.map(x=>x.id)'):
   page.locator('#'+node).click();assert page.locator('#node-detail').inner_text().strip();no_overflow(page,width,('node',node))
  # Keyboard activation on an actual query cell.
  page.locator('#cohort-select').select_option('200m');page.locator('#cell-q04-clickhouse_ec2').focus();page.keyboard.press('Enter');assert page.evaluate('OA.currentRecord().label')=='q04-countrysets'
  page.locator('#inspector').scroll_into_view_if_needed();page.screenshot(path=str(H/f'inspector-{width}.png'),full_page=False)
  page.locator('#explorer').scroll_into_view_if_needed();page.screenshot(path=str(H/f'explorer-{width}.png'),full_page=False)
  viewport_results.append({'width':width,'all205_profiles_real_controls_exact_sql':True,'no_page_overflow':True,'utf8_and_standards':True,'keyboard':True,'flow_nodes':True})
 # Clipboard tests use a mock in this isolated headless test browser, not the user's OS clipboard.
 page.locator('#cohort-select').select_option('200m');page.locator('#cell-q02-clickhouse_ec2').click();sql=page.locator('#sql-body').text_content()
 page.evaluate('Object.defineProperty(navigator,"clipboard",{configurable:true,value:{writeText:async(s)=>{window.__copied=s}}})')
 page.locator('#copy-sql').click();page.wait_for_function('window.__copied!==undefined');assert page.evaluate('window.__copied')==sql
 page.evaluate('Object.defineProperty(navigator,"clipboard",{configurable:true,value:{writeText:async()=>{throw new Error("denied for QA")}}})')
 page.locator('#copy-sql').click();page.wait_for_timeout(150);assert any(s in page.locator('#copy-status').inner_text().lower() for s in ['failed','unavailable','denied'])
 assert not errors,errors
 browser.close()
assert hashlib.sha256(HTML.read_bytes()).hexdigest()==before,'Author changed source during the check; rerun on settled source'
result={'html_sha256':before,'payload_equal':True,'profile_viewport_checks':checked,'exact_sql_viewport_checks':sql_checked,'viewports':viewport_results,'clipboard_mock_success_and_denied':True,'javascript_errors':errors,'scope':'Local real headless Chrome on the authored HTML, not a hosted sharing/access claim.'}
(H/'qa-browser.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
