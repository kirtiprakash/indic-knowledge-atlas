'use strict';
let claims=[];
const $=id=>document.getElementById(id);
const escapeHTML=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function retrieve(q,school=''){
 const tokens=(q.toLocaleLowerCase().match(/[\p{L}\p{N}]+/gu)||[]).filter(t=>t.length>=3&&!['what','does','the','and','how','are','for','about','compare','between','differ','from','this','with'].includes(t));
 return claims.filter(c=>!school||c.school===school).map(c=>{
 const text=[c.claim,c.concept,c.school,...c.tags].join(' ').toLocaleLowerCase();
 const score=tokens.reduce((sum,t)=>sum+(text.includes(t)?1:0),0);
 return {c,score};}).filter(x=>x.score>0).sort((a,b)=>b.score-a.score||a.c.id.localeCompare(b.c.id)).slice(0,6).map(x=>x.c);
}
function render(){const q=$('question').value.trim(),school=$('school').value;const found=retrieve(q,school);const el=$('results');
 if(!q){el.innerHTML='<div class="gap">Enter a question to explore candidate interpretations.</div>';return;}
 if(!found.length){el.innerHTML='<div class="gap"><strong>Knowledge gap</strong><p>There is no matching candidate interpretation in this pilot corpus. No answer or citation has been invented.</p></div>';return;}
 el.innerHTML=found.map(c=>`<article class="result-card"><div class="school">${escapeHTML(c.school)}</div><h3>${escapeHTML(c.concept)}</h3><p>${escapeHTML(c.claim)}</p><div class="source"><b>Source lead:</b> ${escapeHTML(c.source)}<br/><b>Locator:</b> ${escapeHTML(c.locator)}${c.url?` · <a href="${encodeURI(c.url)}" rel="noopener noreferrer" target="_blank">Open reference lead ↗</a>`:''}</div><span class="flag">⚠ Source passage not verified</span></article>`).join('');
}
$('ask').addEventListener('click',render);$('question').addEventListener('keydown',e=>{if(e.key==='Enter')render();});$('school').addEventListener('change',render);document.querySelectorAll('[data-question]').forEach(b=>b.addEventListener('click',()=>{$('question').value=b.dataset.question;render();}));
$('run-tests').addEventListener('click',()=>{const tests=[['Missing evidence abstention',retrieve('xyzzy qqq blorb').length===0],['School-filter correctness',retrieve('liberation','Dvaita Vedānta').every(c=>c.school==='Dvaita Vedānta')],['No verified example asserted',claims.every(c=>c.status!=='verified')],['Source lead explicitly flagged',claims.every(c=>c.status==='illustrative-unverified')]];$('test-output').textContent=tests.map(([name,pass])=>`${pass?'PASS':'FAIL'}  ${name}`).join('\n')+`\n\n${tests.filter(x=>x[1]).length}/${tests.length} checks passed.\nThis is a smoke test, not philosophical validation.`;});
fetch('claims.json').then(r=>{if(!r.ok)throw Error('HTTP '+r.status);return r.json();}).then(data=>{claims=data;$('m-total').textContent=claims.length;$('m-verified').textContent=claims.filter(c=>c.status==='verified').length;$('m-gaps').textContent=claims.filter(c=>c.status!=='verified').length;render();}).catch(()=>{$('results').innerHTML='<div class="gap">Unable to load claims.json. Serve the docs folder over HTTP rather than opening index.html directly.</div>';});
