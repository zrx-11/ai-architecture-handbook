from pathlib import Path
FILES=[Path('index.html'),Path('34-understanding-deep-learning/udl学习伴侣.html')]
FN=r'''function wrapBareMath(root){
  if(!root) return;
  const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT,{
    acceptNode(node){
      if(!node.nodeValue) return NodeFilter.FILTER_REJECT;
      if(node.parentElement && node.parentElement.closest('.katex,.katex-inline,.katex-block')) return NodeFilter.FILTER_REJECT;
      return /\\\(|\\\[/.test(node.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
    }
  });
  const nodes=[]; while(walker.nextNode()) nodes.push(walker.currentNode);
  nodes.forEach(node=>{
    const text=node.nodeValue, frag=document.createDocumentFragment();
    const re=/\\\[([\s\S]*?)\\\]|\\\(([\s\S]*?)\\\)/g;
    let last=0, m;
    while((m=re.exec(text))){
      if(m.index>last) frag.appendChild(document.createTextNode(text.slice(last,m.index)));
      const el=document.createElement(m[1]!==undefined?'div':'span');
      el.className=m[1]!==undefined?'katex-block':'katex-inline';
      el.textContent=(m[1]!==undefined?m[1]:m[2]).trim();
      frag.appendChild(el); last=re.lastIndex;
    }
    if(last<text.length) frag.appendChild(document.createTextNode(text.slice(last)));
    node.parentNode.replaceChild(frag,node);
  });
}
'''
for p in FILES:
 s=p.read_text(encoding='utf-8')
 if 'function wrapBareMath' not in s:
  marker='function renderMath(){'
  assert marker in s,p
  s=s.replace(marker,FN+marker,1)
 if p.name=='index.html':
  old="  $('#view').innerHTML=html;"
  if 'wrapBareMath(document.getElementById(\'view\'));' not in s:
   assert old in s,p
   s=s.replace(old,old+"\n  wrapBareMath(document.getElementById('view'));",1)
 else:
  old="$('#view').innerHTML = html;"
  if 'wrapBareMath(document.getElementById(\'view\'));' not in s:
   assert old in s,p
   s=s.replace(old,old+"\n  wrapBareMath(document.getElementById('view'));",1)
 p.write_text(s,encoding='utf-8')
 print('patched',p)
