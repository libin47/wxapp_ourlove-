"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[836],{48836:function(e,n,o){o.r(n),o.d(n,{default:function(){return j}});var i=o(57437),t=o(20345),r=o.n(t),s=o(2265),c=o(80881),a=o(22649),l=o(52269);async function d(e,n,o){let i=await fetch(a.Y+"/coc_group_add_pc",{method:"POST",headers:{"Content-Type":"text/plain;charset=UTF-8"},body:JSON.stringify({user:n,group:o,data:e})}),t=await i.json();return console.log(t),t.ok}async function u(e,n){let o=await fetch(a.Y+"/coc_group_add_tem",{method:"POST",headers:{"Content-Type":"text/plain;charset=UTF-8"},body:JSON.stringify({group:n,data:e})}),i=await o.json();return console.log(i),i.ok}async function h(e,n){let o=await fetch(a.Y+"/coc_group_del_tem",{method:"POST",headers:{"Content-Type":"text/plain;charset=UTF-8"},body:JSON.stringify({group:n,card_id:e})});return(await o.json()).ok}async function m(e,n){let o=await fetch(a.Y+"/coc_group_update",{method:"POST",headers:{"Content-Type":"text/plain;charset=UTF-8"},body:JSON.stringify({card_id:n,data:e})});return(await o.json()).ok}async function p(e,n,o){let i=await fetch(a.Y+"/coc_group_link_pc",{method:"POST",headers:{"Content-Type":"text/plain;charset=UTF-8"},body:JSON.stringify({card_id:o,user:n,group:e})});return(await i.json()).ok}function x(e){let{group:n,user:o,pcid:t,data:s,hero:l}=e,u=function(e){let i=s[e];i.hero!=l&&(i.hero||l)?c.u_.confirm({content:"该卡与当前群规的英雄类别不一致，是否继续？",onConfirm(){p(n,o,i._id).then(e=>{e&&c.u_.alert({content:"已成功关联！",onConfirm(){window.location.reload()}})})},onClose(){}}):p(n,o,i._id).then(e=>{e&&c.u_.alert({content:"已成功关联！",onConfirm(){window.location.reload()}})})},h=function(e){let i=s[e];i.hero!=l&&(i.hero||l)?c.u_.confirm({content:"该卡与当前群规的英雄类别不一致，是否继续？",onConfirm(){t?m(i,t).then(e=>{e&&c.u_.alert({content:"复制并覆盖当前群角色卡！",onConfirm(){window.location.reload()}})}):d(i,o,n).then(e=>{e&&c.u_.alert({content:"复制并新建到本群角色卡！",onConfirm(){window.location.reload()}})})},onClose(){}}):t?m(i,t).then(e=>{e&&c.u_.alert({content:"复制并覆盖当前群角色卡！",onConfirm(){window.location.reload()}})}):d(i,o,n).then(e=>{e&&c.u_.alert({content:"复制并新建到本群角色卡！",onConfirm(){window.location.reload()}})})};return(0,i.jsx)(i.Fragment,{children:(0,i.jsxs)("div",{className:r().cardbg,children:[(0,i.jsx)("div",{children:"我的角色卡"}),s.map((e,n)=>(0,i.jsxs)("div",{className:r().onecard,style:{backgroundColor:e.group?"lightgoldenrodyellow":"white"},children:[(0,i.jsxs)("div",{className:r().cardLeft,onClick:()=>window.location.href=a.S+"show?pcid="+e._id,children:[e.group?(0,i.jsxs)("div",{children:["来自群：",e.group.map(e=>e)]}):(0,i.jsx)(i.Fragment,{}),(0,i.jsxs)("div",{children:["[",e.info.time?e.info.time:"年代未知"," / ",e.info.wherelive?e.info.wherelive:"居住地未知","]"]}),(0,i.jsxs)("div",{children:["女"===e.info.sex?"♀️":"♂️",e.name," - ",e["职业"],e.hero?" - \uD83E\uDDB8"+e.hero:""]})]}),(0,i.jsxs)("div",{className:r().cardRight,children:[(0,i.jsx)(c.zx,{color:"primary",onClick:()=>u(n),children:"关联"}),(0,i.jsx)(c.zx,{color:"success",onClick:()=>h(n),children:"复制"})]})]},n))]})})}function f(e){let{group:n,user:o,pcid:t,hero:l}=e,[u,h]=(0,s.useState)({group:[],admin:[]}),p=function(e){e.hero!=l&&(e.hero||l)?c.u_.confirm({content:"该卡与当前群规的英雄类别不一致，是否继续？",onConfirm(){t?m(e,t).then(e=>{e&&c.u_.alert({content:"已成功提交！",onConfirm(){window.location.reload()}})}):d(e,o,n).then(e=>{e&&c.u_.alert({content:"已成功提交！",onConfirm(){window.location.reload()}})})},onClose(){}}):t?m(e,t).then(e=>{e&&c.u_.alert({content:"已成功提交！",onConfirm(){window.location.reload()}})}):d(e,o,n).then(e=>{e&&c.u_.alert({content:"已成功提交！",onConfirm(){window.location.reload()}})})},x=async e=>{let n=await fetch(a.Y+"/coc_group_get_tem",{method:"post",headers:{"Content-Type":"text/plain;charset=UTF-8"},body:JSON.stringify({group:e})});h((await n.json()).data)};return(0,s.useEffect)(()=>{x(n)},[]),(0,i.jsx)(i.Fragment,{children:(0,i.jsxs)("div",{className:r().cardbg2,children:[(0,i.jsx)("div",{children:"COC7th预设角色卡"}),u.admin.length>0?u.admin.map((e,n)=>(0,i.jsxs)("div",{className:r().onecard,children:[(0,i.jsxs)("div",{className:r().cardLeft,onClick:()=>window.location.href=a.S+"show?pcid="+e._id,children:[(0,i.jsxs)("div",{children:["[",e.info.time?e.info.time:"年代未知"," / ",e.info.wherelive?e.info.wherelive:"居住地未知","]"]}),(0,i.jsxs)("div",{children:["女"===e.info.sex?"♀️":"♂️",e.name," - ",e["职业"],e.hero?" - \uD83E\uDDB8"+e.hero:""]})]}),(0,i.jsx)("div",{className:r().cardRight,children:(0,i.jsx)(c.zx,{color:"success",onClick:()=>p(e),children:"导入"})})]},e)):(0,i.jsx)("div",{className:r().onecard,children:"暂无模板卡"}),(0,i.jsx)("div",{style:{paddingTop:"32px"},children:"本群预设角色卡"}),u.group.length>0?u.group.map((e,n)=>(0,i.jsxs)("div",{className:r().onecard,onClick:()=>window.location.href=a.S+"show?pcid="+e._id,children:[(0,i.jsxs)("div",{className:r().cardLeft,children:[(0,i.jsxs)("div",{children:["[",e.info.time?e.info.time:"年代未知"," / ",e.info.wherelive?e.info.wherelive:"居住地未知","]"]}),(0,i.jsxs)("div",{children:["女"===e.info.sex?"♀️":"♂️",e.name," - ",e["职业"],e.hero?" - \uD83E\uDDB8"+e.hero:""]})]}),(0,i.jsx)("div",{className:r().cardRight,children:(0,i.jsx)(c.zx,{color:"success",onClick:()=>p(e),children:"导入"})})]},e)):(0,i.jsx)("div",{className:r().onecard,children:"暂无模板卡"})]})})}function g(e){let{group:n,pointAtt:o,attTime:t,heroLevel:d}=e,[p,x]=(0,s.useState)({group:[],admin:[]}),[f,g]=(0,s.useState)(""),[j,_]=(0,s.useState)(!1),w=async e=>{let n=await fetch(a.Y+"/coc_group_get_tem",{method:"post",headers:{"Content-Type":"text/plain;charset=UTF-8"},body:JSON.stringify({group:e})});x((await n.json()).data)};(0,s.useEffect)(()=>{w(n)},[]);let v=e=>{c.Vq.confirm({content:"确认删除？",onConfirm:async()=>{h(e,n).then(e=>{e&&(c.FN.show({icon:"success",content:"删除成功",position:"bottom"}),w(n))})}})};return(0,i.jsx)(i.Fragment,{children:j?(0,i.jsx)(l.Z,{pointatt:o,atttime:t,pcid:"",completeFun:e=>{u(e,n).then(e=>{e&&c.u_.alert({content:"已成功提交！",onConfirm(){w(n),_(!1)}})})},hero:d}):f?(0,i.jsx)(l.Z,{pointatt:o,atttime:t,pcid:f,completeFun:e=>{m(e,f).then(e=>{e&&c.u_.alert({content:"已成功提交！",onConfirm(){g(""),w(n)}})})}}):(0,i.jsx)(function(){return(0,i.jsx)(i.Fragment,{children:(0,i.jsx)("div",{className:r().mainbg,children:(0,i.jsxs)("div",{className:r().cardbg2,children:[(0,i.jsx)("div",{style:{display:"flex",justifyContent:"center",fontSize:"22px"},children:"群模板卡管理"}),p.group.length>0?p.group.map((e,n)=>(0,i.jsx)(i.Fragment,{children:(0,i.jsxs)("div",{className:r().onecard,children:[(0,i.jsxs)("div",{className:r().cardLeft,onClick:()=>window.location.href=a.S+"show?pcid="+e._id,children:[(0,i.jsxs)("div",{children:["[",e.info.time?e.info.time:"年代未知"," / ",e.info.wherelive?e.info.wherelive:"居住地未知","]"]}),(0,i.jsxs)("div",{children:["女"===e.info.sex?"♀️":"♂️",e.name," - ",e["职业"],e.hero?" - \uD83E\uDDB8"+e.hero:""]})]}),(0,i.jsxs)("div",{className:r().cardRight,children:[(0,i.jsx)(c.zx,{color:"success",onClick:()=>g(e._id),children:"编辑"}),(0,i.jsx)(c.zx,{color:"danger",onClick:()=>v(e._id),style:{marginLeft:8},children:"删除"})]})]},e)})):(0,i.jsx)("div",{className:r().onecard,children:"暂无模板卡，点击下面按钮创建"}),(0,i.jsx)(c.zx,{block:!0,color:"primary",onClick:()=>_(!0),style:{marginTop:16},children:"新增"}),(0,i.jsx)(c.zx,{block:!0,color:"warning",onClick:()=>window.location.reload(),style:{marginTop:8},children:"返回"})]})})})},{})})}function j(){let[e,n]=(0,s.useState)(500),[o,t]=(0,s.useState)(5),[u,h]=(0,s.useState)(0),[p,j]=(0,s.useState)(""),[_,w]=(0,s.useState)(""),[v,C]=(0,s.useState)(!1),[y,N]=(0,s.useState)(!1),[k,S]=(0,s.useState)(!1),[T,b]=(0,s.useState)(!1),[F,z]=(0,s.useState)(),D=async e=>{let n=e.group,o=e.user,i=await fetch(a.Y+"/coc_group_get_user",{method:"post",headers:{"Content-Type":"text/plain;charset=UTF-8"},body:JSON.stringify({user:o,group:n})}),t=(await i.json()).data;0===t.user.length&&0===t.user_group.length||z(t)},O=async e=>{let o=e.group,i=await fetch(a.Y+"/coc_group_config?group="+o,{method:"get",headers:{"Content-Type":"text/plain;charset=UTF-8"}}),r=(await i.json()).data,s=+r.point?+r.point:500,c=+r.dicetime?+r.dicetime:5,l=+r.hero?+r.hero:0;t(c),n(s),h(l)};(0,s.useEffect)(()=>{let e=window.location.search.split("?")[1];var n=e?e.split("&"):[],o={};for(let e=0;e<n.length;e++){let i=n[e].split("=");o[i[0]]=i[1]}o.user?D(o):b(!0),O(o),w(o.group),j(o.user)},[]);let E=e=>{d(e,p,_).then(e=>{c.u_.alert({content:"已成功提交！",onConfirm(){window.location.reload()}})})},U=e=>{m(e,null==F?void 0:F.user_group._id).then(e=>{e&&c.u_.alert({content:"已成功提交！",onConfirm(){C(!1),D({group:_})}})})};function Y(){return(0,i.jsxs)("div",{className:r().mainbg,children:[(0,i.jsx)(x,{group:_,user:p,pcid:null==F?void 0:F.user_group._id,data:F?F.user:[],hero:u}),(0,i.jsxs)("div",{className:r().cardbg,children:[(0,i.jsx)("div",{children:"本群我的角色卡"}),(null==F?void 0:F.user_group.name)?(0,i.jsxs)("div",{className:r().onecard,children:[(0,i.jsxs)("div",{className:r().cardLeft,onClick:()=>window.location.href=a.S+"show?pcid="+(null==F?void 0:F.user_group._id),children:[(0,i.jsxs)("div",{children:["[",(null==F?void 0:F.user_group.info.time)?null==F?void 0:F.user_group.info.time:"年代未知"," / ",(null==F?void 0:F.user_group.info.wherelive)?null==F?void 0:F.user_group.info.wherelive:"居住地未知","]"]}),(0,i.jsxs)("div",{children:[(null==F?void 0:F.user_group.info.sex)==="女"?"♀️":"♂️",null==F?void 0:F.user_group.name," - ",null==F?void 0:F.user_group["职业"],(null==F?void 0:F.user_group.hero)?" - \uD83E\uDDB8"+(null==F?void 0:F.user_group.hero):""," "]})]}),(0,i.jsx)("div",{className:r().cardRight,children:(0,i.jsx)(c.zx,{color:"success",onClick:()=>{C(!0)},children:"编辑"})})]}):(0,i.jsx)(i.Fragment,{})]}),(0,i.jsx)("div",{children:(0,i.jsx)(c.zx,{block:!0,color:"success",size:"large",onClick:()=>{N(!0)},children:"新建角色卡"})}),(0,i.jsx)("div",{children:(0,i.jsx)(c.zx,{block:!0,color:"success",size:"large",onClick:()=>{S(!0)},style:{marginTop:16},children:"导入预设卡"})})]})}return(0,i.jsx)(i.Fragment,{children:T?(0,i.jsx)(g,{group:_,pointAtt:e,attTime:o,heroLevel:u}):k?(0,i.jsx)(function(){return(0,i.jsx)(i.Fragment,{children:(0,i.jsxs)("div",{className:r().mainbg2,children:[(0,i.jsx)(f,{group:_,user:p,pcid:null==F?void 0:F.user_group._id,hero:u}),(0,i.jsx)("div",{children:(0,i.jsx)(c.zx,{block:!0,color:"success",size:"large",onClick:()=>{S(!1)},style:{marginTop:32},children:"返回"})}),(0,i.jsxs)("div",{className:r().newtemtext,children:[" ",(0,i.jsx)("div",{onClick:()=>{b(!0)},children:"模板管理"})," "]})]})})},{}):(0,i.jsx)(function(){return(0,i.jsx)(i.Fragment,{children:y?(0,i.jsx)(l.Z,{pointatt:e,atttime:o,hero:u,pcid:"",completeFun:E}):v?(0,i.jsx)(l.Z,{pointatt:e,atttime:o,pcid:null==F?void 0:F.user_group._id,completeFun:U}):(0,i.jsx)(Y,{})})},{})})}}}]);