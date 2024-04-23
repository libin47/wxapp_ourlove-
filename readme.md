netstat -tunlp|grep 7684 查看端口占用
ctrl+z
bg 1
disown -h %1


## 数据结构
```shell
Group:
  _id: string,
  status: bool,
  Gaming: bool,
  config: {dicetime:10,failnum:-1,point:500,succnum:-1},
  card: {wxid: pcid},   -> PcCard._id
  group_card: string[]   -> PcCard._id
  
User:
  _id: string,
  wxid: string,
  pc: string[]  -> PcCard._id
  
PcCard:
  _id: string,
  name: string,
  owner: string, -> User._id
  group: string[],  -> Group._id
  info: ,
  职业: string,
  attribute: ,
  attex: ,
  skill: ,
  skill_work: ,
  story: ,
  CR: ,
  weapon: ,

  
  

```