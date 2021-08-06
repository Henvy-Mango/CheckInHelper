## Configuration file template

It is recommended to copy and rename `config.example.json` to `config.json` before use configuration file.

### config.example.json

```json
{
  "//": "iOS Bark app's IP or device code. For example: https://api.day.app/xxxxxx",
  "BARK_KEY": "",
  "//": "iOS Bark app's notification sound. Default: healthnotification",
  "BARK_SOUND": "healthnotification",
  "//": "SKEY for Cool Push. See: https://cp.xuthus.cc/",
  "COOL_PUSH_SKEY": "",
  "//": "Push method for Cool Push. Choose from send(私聊)|group(群组)|wx(微信). Default: send",
  "COOL_PUSH_MODE": "send",
  "//": "Custom notifier configuration",
  "CUSTOM_NOTIFIER": {
    "method": "post",
    "url": "",
    "data": {
    },
    "retcode_key": "",
    "retcode_value": 200,
    "data_type": "data",
    "merge_title_and_desp": false,
    "set_data_title": "",
    "set_data_sub_title": "",
    "set_data_desp": ""
  },
  "//": "钉钉机器人WebHook地址中access_token后的字段.",
  "DD_BOT_TOKEN": "",
  "//": "钉钉加签密钥.在机器人安全设置页面,加签一栏下面显示的以SEC开头的字符串.",
  "DD_BOT_SECRET": "",
  "//": "KEY for iGot. For example: https://push.hellyw.com/xxxxxx",
  "IGOT_KEY": "",
  "//": "pushplus 一对一推送或一对多推送的token.不配置push_plus_user则默认为一对一推送.详见文档: https://www.pushplus.plus/doc/",
  "PUSH_PLUS_TOKEN": "",
  "//": "pushplus 一对多推送的群组编码.在'一对多推送'->'您的群组'(如无则新建)->'群组编码'里查看,如果是创建群组人,也需点击'查看二维码'扫描绑定,否则不能接收群组消息.",
  "PUSH_PLUS_USER": "",
  "//": "SCKEY for ServerChan. See: https://sc.ftqq.com/3.version",
  "SCKEY": "",
  "//": "SENDKEY for ServerChanTurbo. See: https://sct.ftqq.com/",
  "SCTKEY": "",
  "//": "Telegram robot api address. Default: api.telegram.org",
  "TG_BOT_API": "api.telegram.org",
  "//": "Telegram robot token. Generated when requesting a bot from @botfather",
  "TG_BOT_TOKEN": "",
  "//": "User ID of the Telegram push target.",
  "TG_USER_ID": "",
  "//": "企业微信的企业ID(corpid).在'管理后台'->'我的企业'->'企业信息'里查看.详见文档: https://work.weixin.qq.com/api/doc/90000/90135/90236",
  "WW_ID": "",
  "//": "企业微信应用的secret.在'管理后台'->'应用与小程序'->'应用'->'自建',点进某应用里查看.",
  "WW_APP_SECRET": "",
  "//": "企业微信应用推送对象的用户ID.在'管理后台'->' 通讯录',点进某用户的详情页里查看.默认: @all",
  "WW_APP_USERID": "@all",
  "//": "企业微信应用的agentid.在'管理后台'->'应用与小程序'->'应用',点进某应用里查看.",
  "WW_APP_AGENTID": "",
  "//": "企业微信机器人WebHook地址中key后的字段.详见文档: https://work.weixin.qq.com/api/doc/90000/90136/91770",
  "WW_BOT_KEY": ""
}
```

### Custom notifier configuration

```json
{
  "method": "post",
  "url": "",
  "data": {
  },
  "retcode_key": "",
  "retcode_value": 200,
  "data_type": "data",
  "merge_title_and_desp": false,
  "set_data_title": "",
  "set_data_sub_title": "",
  "set_data_desp": ""
}
```

```
Custom notifier:
    method:                 Required, the request method. Default: post.
    url:                    Required, the full custom push link.
    data:                   Optional, the data to sent. default: {}, you can add additional parameters.
    retcode_key:            Required, the key of the status code returned by the response body.
    retcode_value:          Required, the value of the status code returned by the response body.
    data_type:              Optional, the way to send data, choose from params|json|data, default: data.
    merge_title_and_desp:   Optional, if or not the title (application name + running status) and the running result will be merged. Default: false.
    set_data_title:         Required, the key of the message title in the data of the push method.
    set_data_sub_title:     Optional, the key of the message body in the push data.
    set_data_desp:          Optional, the key of the message body in the push data.

自定义推送:
    method:                 必填,请求方式.默认: post.
    url:                    必填,完整的自定义推送链接.
    data:                   选填,发送的data.默认为空,可自行添加额外参数.
    retcode_key:            必填,响应体返回的状态码的key.
    retcode_value:          必填,响应体返回的状态码的value.
    data_type:              选填,发送data的方式,可选params|json|data,默认: data.
    merge_title_and_desp:   选填,是否将标题(应用名+运行状态)和运行结果合并.默认: false.
    set_data_title:         必填,推送方式data中消息标题的key.
    set_data_sub_title:     选填,推送方式data中消息正文的key.有的推送方式正文的key有次级结构,需配合set_data_title构造子级,与set_data_desp互斥.
                                例如: 企业微信中,set_data_title填text,set_data_sub_title填content.
    set_data_desp:          选填,推送方式data中消息正文的key.例如: server酱的为desp.
                                与set_data_sub_title互斥,两者都填则本项不生效.
```

例子： 写一个 ServerChan 的自定义推送。

查看文档得到 ServerChan 推送所需要的信息： 需要的`url`形式为：`https://sc.ftqq.com/{SCKEY}.send`
发送的`data`形式为：`{'text': test','desp':desp}`
消息发送成功响应体为：`{'errno': 0, 'errmsg': 'OK'}`

自定义推送配置如下：

```
{
    "method":"post",
    "url":"https://sc.ftqq.com/{直接填写你的SCKEY}.send",
    "data":{
      
    },
    "retcode_key":"errno",
    "retcode_value":0,
    "data_type":"data",
    "merge_title_and_desp":true,
    "set_data_title":"test",
    "set_data_sub_title":"",
    "set_data_desp":"desp"
}
```
