var me=Object.defineProperty;var be=(t,e,r)=>e in t?me(t,e,{enumerable:!0,configurable:!0,writable:!0,value:r}):t[e]=r;var Q=(t,e,r)=>be(t,typeof e!="symbol"?e+"":e,r);(function(){const e=document.createElement("link").relList;if(e&&e.supports&&e.supports("modulepreload"))return;for(const l of document.querySelectorAll('link[rel="modulepreload"]'))n(l);new MutationObserver(l=>{for(const u of l)if(u.type==="childList")for(const s of u.addedNodes)s.tagName==="LINK"&&s.rel==="modulepreload"&&n(s)}).observe(document,{childList:!0,subtree:!0});function r(l){const u={};return l.integrity&&(u.integrity=l.integrity),l.referrerPolicy&&(u.referrerPolicy=l.referrerPolicy),l.crossOrigin==="use-credentials"?u.credentials="include":l.crossOrigin==="anonymous"?u.credentials="omit":u.credentials="same-origin",u}function n(l){if(l.ep)return;l.ep=!0;const u=r(l);fetch(l.href,u)}})();function O(){}function pe(t){return t()}function re(){return Object.create(null)}function P(t){t.forEach(pe)}function ge(t){return typeof t=="function"}function H(t,e){return t!=t?e==e:t!==e||t&&typeof t=="object"||typeof t=="function"}function we(t){return Object.keys(t).length===0}function _(t,e){t.appendChild(e)}function $(t,e,r){t.insertBefore(e,r||null)}function y(t){t.parentNode&&t.parentNode.removeChild(t)}function R(t,e){for(let r=0;r<t.length;r+=1)t[r]&&t[r].d(e)}function m(t){return document.createElement(t)}function D(t){return document.createTextNode(t)}function q(){return D(" ")}function W(){return D("")}function ne(t,e,r,n){return t.addEventListener(e,r,n),()=>t.removeEventListener(e,r,n)}function p(t,e,r){r==null?t.removeAttribute(e):t.getAttribute(e)!==r&&t.setAttribute(e,r)}function ye(t){return Array.from(t.childNodes)}function he(t,e){e=""+e,t.data!==e&&(t.data=e)}function le(t,e){t.value=e??""}let Z;function I(t){Z=t}const C=[],oe=[];let S=[];const se=[],xe=Promise.resolve();let Y=!1;function $e(){Y||(Y=!0,xe.then(_e))}function K(t){S.push(t)}const V=new Set;let B=0;function _e(){if(B!==0)return;const t=Z;do{try{for(;B<C.length;){const e=C[B];B++,I(e),ke(e.$$)}}catch(e){throw C.length=0,B=0,e}for(I(null),C.length=0,B=0;oe.length;)oe.pop()();for(let e=0;e<S.length;e+=1){const r=S[e];V.has(r)||(V.add(r),r())}S.length=0}while(C.length);for(;se.length;)se.pop()();Y=!1,V.clear(),I(t)}function ke(t){if(t.fragment!==null){t.update(),P(t.before_update);const e=t.dirty;t.dirty=[-1],t.fragment&&t.fragment.p(t.ctx,e),t.after_update.forEach(K)}}function ve(t){const e=[],r=[];S.forEach(n=>t.indexOf(n)===-1?e.push(n):r.push(n)),r.forEach(n=>n()),S=e}const U=new Set;let L;function T(){L={r:0,c:[],p:L}}function M(){L.r||P(L.c),L=L.p}function h(t,e){t&&t.i&&(U.delete(t),t.i(e))}function b(t,e,r,n){if(t&&t.o){if(U.has(t))return;U.add(t),L.c.push(()=>{U.delete(t),n&&(r&&t.d(1),n())}),t.o(e)}else n&&n()}function j(t){return(t==null?void 0:t.length)!==void 0?t:Array.from(t)}function A(t){t&&t.c()}function N(t,e,r){const{fragment:n,after_update:l}=t.$$;n&&n.m(e,r),K(()=>{const u=t.$$.on_mount.map(pe).filter(ge);t.$$.on_destroy?t.$$.on_destroy.push(...u):P(u),t.$$.on_mount=[]}),l.forEach(K)}function E(t,e){const r=t.$$;r.fragment!==null&&(ve(r.after_update),P(r.on_destroy),r.fragment&&r.fragment.d(e),r.on_destroy=r.fragment=null,r.ctx=[])}function qe(t,e){t.$$.dirty[0]===-1&&(C.push(t),$e(),t.$$.dirty.fill(0)),t.$$.dirty[e/31|0]|=1<<e%31}function F(t,e,r,n,l,u,s=null,c=[-1]){const i=Z;I(t);const o=t.$$={fragment:null,ctx:[],props:u,update:O,not_equal:l,bound:re(),on_mount:[],on_destroy:[],on_disconnect:[],before_update:[],after_update:[],context:new Map(e.context||(i?i.$$.context:[])),callbacks:re(),dirty:c,skip_bound:!1,root:e.target||i.$$.root};s&&s(o.root);let f=!1;if(o.ctx=r?r(t,e.props||{},(d,g,...a)=>{const x=a.length?a[0]:g;return o.ctx&&l(o.ctx[d],o.ctx[d]=x)&&(!o.skip_bound&&o.bound[d]&&o.bound[d](x),f&&qe(t,d)),g}):[],o.update(),f=!0,P(o.before_update),o.fragment=n?n(o.ctx):!1,e.target){if(e.hydrate){const d=ye(e.target);o.fragment&&o.fragment.l(d),d.forEach(y)}else o.fragment&&o.fragment.c();e.intro&&h(t.$$.fragment),N(t,e.target,e.anchor),_e()}I(i)}class G{constructor(){Q(this,"$$");Q(this,"$$set")}$destroy(){E(this,1),this.$destroy=O}$on(e,r){if(!ge(r))return O;const n=this.$$.callbacks[e]||(this.$$.callbacks[e]=[]);return n.push(r),()=>{const l=n.indexOf(r);l!==-1&&n.splice(l,1)}}$set(e){this.$$set&&!we(e)&&(this.$$.skip_bound=!0,this.$$set(e),this.$$.skip_bound=!1)}}const Oe="4";typeof window<"u"&&(window.__svelte||(window.__svelte={v:new Set})).v.add(Oe);function ie(t,e,r){const n=t.slice();return n[2]=e[r],n[4]=r,n}function ue(t){let e,r,n,l;return{c(){e=m("a"),r=m("span"),r.textContent=`reference: ${t[4]}`,p(e,"href",n=t[2]),p(e,"rel","discussion"),p(e,"title",l=t[2]),p(e,"accesskey","t")},m(u,s){$(u,e,s),_(e,r)},p(u,s){s&1&&n!==(n=u[2])&&p(e,"href",n),s&1&&l!==(l=u[2])&&p(e,"title",l)},d(u){u&&y(e)}}}function Ne(t){let e,r,n,l,u,s,c,i,o=j(t[0]),f=[];for(let d=0;d<o.length;d+=1)f[d]=ue(ie(t,o,d));return{c(){e=m("div"),r=m("div"),n=m("div"),l=m("div"),l.innerHTML='<span class="text-sm font-semibold text-gray-900 dark:text-white">Bot</span> <span class="text-sm font-normal text-gray-500 dark:text-gray-400">11:46</span>',u=q(),s=m("p"),c=D(t[1]),i=q();for(let d=0;d<f.length;d+=1)f[d].c();p(l,"class","flex items-center space-x-2 rtl:space-x-reverse"),p(s,"class","py-2.5 text-sm font-normal text-gray-900 dark:text-white"),p(n,"class","leading-1.5 flex w-full max-w-[320px] flex-col rounded-r-xl rounded-bl-xl border-gray-200 bg-gray-200 p-4 dark:bg-gray-700"),p(r,"class","flex items-start gap-2.5 pl-2"),p(e,"class","grid gap-4")},m(d,g){$(d,e,g),_(e,r),_(r,n),_(n,l),_(n,u),_(n,s),_(s,c),_(n,i);for(let a=0;a<f.length;a+=1)f[a]&&f[a].m(n,null)},p(d,[g]){if(g&2&&he(c,d[1]),g&1){o=j(d[0]);let a;for(a=0;a<o.length;a+=1){const x=ie(d,o,a);f[a]?f[a].p(x,g):(f[a]=ue(x),f[a].c(),f[a].m(n,null))}for(;a<f.length;a+=1)f[a].d(1);f.length=o.length}},i:O,o:O,d(d){d&&y(e),R(f,d)}}}function Ee(t,e,r){let{answer:n}=e,{sources:l}=e;return l=l||[],console.log(l),t.$$set=u=>{"answer"in u&&r(1,n=u.answer),"sources"in u&&r(0,l=u.sources)},[l,n]}class z extends G{constructor(e){super(),F(this,e,Ee,Ne,H,{answer:1,sources:0})}}function Le(t){let e,r,n,l,u,s;return{c(){e=m("div"),r=m("div"),n=m("div"),n.innerHTML='<span class="text-sm font-semibold text-gray-900 dark:text-white">User</span> <span class="text-sm font-normal text-gray-500 dark:text-gray-400">11:46</span>',l=q(),u=m("p"),s=D(t[0]),p(n,"class","flex items-center space-x-2 rtl:space-x-reverse"),p(u,"class","py-2.5 text-sm font-normal text-gray-900 dark:text-white"),p(r,"class","leading-1.5 flex w-full max-w-[320px] flex-col rounded-l-xl rounded-br-xl border-gray-200 bg-gray-400 p-4 dark:bg-gray-700"),p(e,"class","flex items-start gap-2.5 pl-2")},m(c,i){$(c,e,i),_(e,r),_(r,n),_(r,l),_(r,u),_(u,s)},p(c,[i]){i&1&&he(s,c[0])},i:O,o:O,d(c){c&&y(e)}}}function Ae(t,e,r){let{question:n}=e;return t.$$set=l=>{"question"in l&&r(0,n=l.question)},[n]}class X extends G{constructor(e){super(),F(this,e,Ae,Le,H,{question:0})}}function ce(t,e,r){const n=t.slice();return n[10]=e[r],n}function fe(t,e,r){const n=t.slice();return n[10]=e[r],n}function Be(t){let e,r,n,l,u,s=j(t[0]),c=[];for(let o=0;o<s.length;o+=1)c[o]=ae(ce(t,s,o));const i=o=>b(c[o],1,1,()=>{c[o]=null});return r=new X({props:{question:t[2]}}),l=new z({props:{answer:t[1],sources:["https://bratislava.sk/vyhladavanie?keyword=266"]}}),{c(){for(let o=0;o<c.length;o+=1)c[o].c();e=q(),A(r.$$.fragment),n=q(),A(l.$$.fragment)},m(o,f){for(let d=0;d<c.length;d+=1)c[d]&&c[d].m(o,f);$(o,e,f),N(r,o,f),$(o,n,f),N(l,o,f),u=!0},p(o,f){if(f&1){s=j(o[0]);let a;for(a=0;a<s.length;a+=1){const x=ce(o,s,a);c[a]?(c[a].p(x,f),h(c[a],1)):(c[a]=ae(x),c[a].c(),h(c[a],1),c[a].m(e.parentNode,e))}for(T(),a=s.length;a<c.length;a+=1)i(a);M()}const d={};f&4&&(d.question=o[2]),r.$set(d);const g={};f&2&&(g.answer=o[1]),l.$set(g)},i(o){if(!u){for(let f=0;f<s.length;f+=1)h(c[f]);h(r.$$.fragment,o),h(l.$$.fragment,o),u=!0}},o(o){c=c.filter(Boolean);for(let f=0;f<c.length;f+=1)b(c[f]);b(r.$$.fragment,o),b(l.$$.fragment,o),u=!1},d(o){o&&(y(e),y(n)),R(c,o),E(r,o),E(l,o)}}}function Ce(t){let e,r,n=j(t[0]),l=[];for(let s=0;s<n.length;s+=1)l[s]=de(fe(t,n,s));const u=s=>b(l[s],1,1,()=>{l[s]=null});return{c(){for(let s=0;s<l.length;s+=1)l[s].c();e=W()},m(s,c){for(let i=0;i<l.length;i+=1)l[i]&&l[i].m(s,c);$(s,e,c),r=!0},p(s,c){if(c&1){n=j(s[0]);let i;for(i=0;i<n.length;i+=1){const o=fe(s,n,i);l[i]?(l[i].p(o,c),h(l[i],1)):(l[i]=de(o),l[i].c(),h(l[i],1),l[i].m(e.parentNode,e))}for(T(),i=n.length;i<l.length;i+=1)u(i);M()}},i(s){if(!r){for(let c=0;c<n.length;c+=1)h(l[c]);r=!0}},o(s){l=l.filter(Boolean);for(let c=0;c<l.length;c+=1)b(l[c]);r=!1},d(s){s&&y(e),R(l,s)}}}function Se(t){let e,r;return e=new X({props:{question:t[10].text}}),{c(){A(e.$$.fragment)},m(n,l){N(e,n,l),r=!0},p(n,l){const u={};l&1&&(u.question=n[10].text),e.$set(u)},i(n){r||(h(e.$$.fragment,n),r=!0)},o(n){b(e.$$.fragment,n),r=!1},d(n){E(e,n)}}}function je(t){let e,r;return e=new z({props:{answer:t[10].text,sources:t[10].sources}}),{c(){A(e.$$.fragment)},m(n,l){N(e,n,l),r=!0},p(n,l){const u={};l&1&&(u.answer=n[10].text),l&1&&(u.sources=n[10].sources),e.$set(u)},i(n){r||(h(e.$$.fragment,n),r=!0)},o(n){b(e.$$.fragment,n),r=!1},d(n){E(e,n)}}}function ae(t){let e,r,n,l;const u=[je,Se],s=[];function c(i,o){return i[10].role==="bot"?0:i[10].role==="user"?1:-1}return~(e=c(t))&&(r=s[e]=u[e](t)),{c(){r&&r.c(),n=W()},m(i,o){~e&&s[e].m(i,o),$(i,n,o),l=!0},p(i,o){let f=e;e=c(i),e===f?~e&&s[e].p(i,o):(r&&(T(),b(s[f],1,1,()=>{s[f]=null}),M()),~e?(r=s[e],r?r.p(i,o):(r=s[e]=u[e](i),r.c()),h(r,1),r.m(n.parentNode,n)):r=null)},i(i){l||(h(r),l=!0)},o(i){b(r),l=!1},d(i){i&&y(n),~e&&s[e].d(i)}}}function Pe(t){let e,r;return e=new X({props:{question:t[10].text}}),{c(){A(e.$$.fragment)},m(n,l){N(e,n,l),r=!0},p(n,l){const u={};l&1&&(u.question=n[10].text),e.$set(u)},i(n){r||(h(e.$$.fragment,n),r=!0)},o(n){b(e.$$.fragment,n),r=!1},d(n){E(e,n)}}}function Ie(t){let e,r;return e=new z({props:{answer:t[10].text,sources:t[10].sources}}),{c(){A(e.$$.fragment)},m(n,l){N(e,n,l),r=!0},p(n,l){const u={};l&1&&(u.answer=n[10].text),l&1&&(u.sources=n[10].sources),e.$set(u)},i(n){r||(h(e.$$.fragment,n),r=!0)},o(n){b(e.$$.fragment,n),r=!1},d(n){E(e,n)}}}function de(t){let e,r,n,l;const u=[Ie,Pe],s=[];function c(i,o){return i[10].role==="bot"?0:i[10].role==="user"?1:-1}return~(e=c(t))&&(r=s[e]=u[e](t)),{c(){r&&r.c(),n=W()},m(i,o){~e&&s[e].m(i,o),$(i,n,o),l=!0},p(i,o){let f=e;e=c(i),e===f?~e&&s[e].p(i,o):(r&&(T(),b(s[f],1,1,()=>{s[f]=null}),M()),~e?(r=s[e],r?r.p(i,o):(r=s[e]=u[e](i),r.c()),h(r,1),r.m(n.parentNode,n)):r=null)},i(i){l||(h(r),l=!0)},o(i){b(r),l=!1},d(i){i&&y(n),~e&&s[e].d(i)}}}function Te(t){let e,r,n,l,u,s,c,i,o,f,d,g,a,x;const ee=[Ce,Be],k=[];function te(w,v){return w[3]?1:0}return r=te(t),n=k[r]=ee[r](t),{c(){e=m("div"),n.c(),l=q(),u=m("div"),s=m("label"),s.textContent="Your message",c=q(),i=m("div"),o=m("textarea"),f=q(),d=m("button"),d.innerHTML='<svg class="h-5 w-5 rotate-90 rtl:-rotate-90" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 18 20"><path d="m17.914 18.594-8-18a1 1 0 0 0-1.828 0l-8 18a1 1 0 0 0 1.157 1.376L8 18.281V9a1 1 0 0 1 2 0v9.281l6.758 1.689a1 1 0 0 0 1.156-1.376Z"></path></svg>',p(e,"class","h-72 overflow-auto p-6 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700"),p(s,"for","chat"),p(s,"class","sr-only"),p(o,"id","chat"),p(o,"rows","3"),p(o,"class","mx-4 block w-full rounded-lg border border-gray-300 bg-white p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-800 dark:text-white dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"),p(o,"placeholder","Your message..."),p(d,"class","inline-flex cursor-pointer justify-center rounded-full p-2 text-blue-600 hover:bg-blue-100 dark:text-blue-500 dark:hover:bg-gray-600"),p(i,"class","flex items-center rounded-lg bg-gray-50 px-3 py-2 dark:bg-gray-700")},m(w,v){$(w,e,v),k[r].m(e,null),$(w,l,v),$(w,u,v),_(u,s),_(u,c),_(u,i),_(i,o),le(o,t[2]),_(i,f),_(i,d),g=!0,a||(x=[ne(o,"input",t[5]),ne(d,"click",t[4])],a=!0)},p(w,[v]){let J=r;r=te(w),r===J?k[r].p(w,v):(T(),b(k[J],1,1,()=>{k[J]=null}),M(),n=k[r],n?n.p(w,v):(n=k[r]=ee[r](w),n.c()),h(n,1),n.m(e,null)),v&4&&le(o,w[2])},i(w){g||(h(n),g=!0)},o(w){b(n),g=!1},d(w){w&&(y(e),y(l),y(u)),k[r].d(),a=!1,P(x)}}}const Me="https://aip-api.shs-net.org/generate-rag?limit=2&stream=False&model=llama3%2E1";function Ue(t,e,r){let n,l,u,s,c,i;async function o(){n!==""&&(console.log(`from ChatDialog; run with prompt: ${n}`),r(3,s=!0),await f(),r(0,c=[...c,{id:i+1,role:"user",text:n},{id:i+2,role:"bot",text:l,sources:u}]),r(1,l=""),u=[],r(2,n=""),r(3,s=!1))}async function f(){const g=await fetch(Me,{method:"POST",headers:{"Content-Type":"application/json; charset=utf-8"},body:JSON.stringify({prompt:n})});if(g&&g.body){const a=await g.json();r(1,l=a.llm_answer),u=a.sources}else r(1,l="Invalid answer")}function d(){n=this.value,r(2,n)}return t.$$.update=()=>{t.$$.dirty&1&&(i=c.length)},r(2,n=""),r(1,l=""),u=[],r(3,s=!1),r(0,c=[{id:1,role:"bot",text:"Welcome from bot!",sources:["https://www.example.org/"]},{id:2,role:"user",text:"User Q"},{id:3,role:"bot",text:"Bot A",sources:["https://www.example.org/"]}]),[c,l,n,s,o,d]}class He extends G{constructor(e){super(),F(this,e,Ue,Te,H,{})}}function De(t){let e,r;return e=new He({}),{c(){A(e.$$.fragment)},m(n,l){N(e,n,l),r=!0},p:O,i(n){r||(h(e.$$.fragment,n),r=!0)},o(n){b(e.$$.fragment,n),r=!1},d(n){E(e,n)}}}class Fe extends G{constructor(e){super(),F(this,e,null,De,H,{})}}new Fe({target:document.getElementById("app")});