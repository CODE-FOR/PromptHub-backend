# 模型表

### 管理员 admin

* username
* password

### 用户 user

* email：unique
* password
* username：nickname
* avatar：图像url
* followers
* is_delete：safe delete
* is_confirmed：邮箱是否验证
* is_banned：是否加入黑名单

### 评论 comment

* prompt
* user
* created_at
* content
* parent_comment
* is_delete：safe delete

### 作品 Prompt

* prompt
* picture：图像url
* model
* width
* height
* uploader
* upload_status：上传状态
    * 已经上架
    * 审核中
    * 下架中
* is_delete：safe delete

### 标签 tag

* Prompt

### 通知 notification

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