# 模型表

### 管理员 admin

* username
* password

### 用户 user

* email：unique
* password
* nickname
* avatar：图像url
* followers
* is_confirmed：邮箱是否验证
* is_banned：是否加入黑名单

### 评论 comment

* prompt
* user
* created_at
* content
* parent_comment

### 作品 Prompt

* prompt
* picture：图像url
* model
* width
* height
* uploader
* created_at
* prompt_attribute
* upload_status：上传状态
    * 已经上架
    * 审核中
    * 下架中

### 通知 notification

* user
* content
* status：read和unread
* created_at

### 浏览历史 history

> 仅保存最近100条

* created_at
* user
* prompt

### 审核记录 audit_record

* created_at
* prompt
* user
* status
* feedback
* is_delete

### 收藏记录 collect_record

* created_at
* prompt
* collection

### 收藏夹 collection

* name
* user
* created_at
* visibility：public和private
* cover：url