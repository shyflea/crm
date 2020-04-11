[TOC]



##  一、简介

1、本框架编写的最主要目的，是为了提供一个快速应用开发框架。
2、采用django+simpleui做为基础框架；sipmpleui是基于element-ui+vue针对django开发的一个开源前端框架。
3、完成了组织员工管理、菜单管理、权限管理、缓存管理、主数据配置、区域配置等功能模块
4、组织、员工、权限模型参考运营商模型，支持对员工、岗位、角色授权
5、缓存使用redis，并提供了缓存可视化页面，能够看到当前缓存情况，能够查看缓存的生失效时间。在生产过程中能够快速定位缓存是否有问题。支持删除缓存，能够全部删除、能够针对某类缓存删除、能够针对具体某一条缓存删除。
6、主数据模型参考运营商主数据模型，由主题域、类、属性、属性值四个维度构成

## 二、功能截图
### 1、首页

![image-20200411182123841](D:\test\git\crm\readme.assets\image-20200411182123841.png)

### 2、组织管理

![image-20200411182537267](D:\test\git\crm\readme.assets\image-20200411182537267.png)

![image-20200411182559241](D:\test\git\crm\readme.assets\image-20200411182559241.png)

### 3、员工管理

 主页面：
 ![image-20200411182810018](D:\test\git\crm\readme.assets\image-20200411182810018.png)
 编辑页面：
![image-20200411182909925](D:\test\git\crm\readme.assets\image-20200411182909925.png)
 授权页面：

![image-20200411183454332](D:\test\git\crm\readme.assets\image-20200411183454332.png)






### 4、菜单管理

![image-20200411183000497](D:\test\git\crm\readme.assets\image-20200411183000497.png)

![image-20200411183037205](D:\test\git\crm\readme.assets\image-20200411183037205.png)

### 5、权限管理
主页面：
![image-20200411183120146](D:\test\git\crm\readme.assets\image-20200411183120146.png)
编辑页面：
![image-20200411183135809](D:\test\git\crm\readme.assets\image-20200411183135809.png)

### 6、岗位配置
主页面：

![image-20200411183525300](D:\test\git\crm\readme.assets\image-20200411183525300.png)

编辑页面：

![image-20200411183541756](D:\test\git\crm\readme.assets\image-20200411183541756.png)

授权：

![image-20200411183613323](D:\test\git\crm\readme.assets\image-20200411183613323.png)

### 7、角色配置
主页面：

![image-20200411183629030](D:\test\git\crm\readme.assets\image-20200411183629030.png)

编辑页面：

![image-20200411183646735](D:\test\git\crm\readme.assets\image-20200411183646735.png)

授权：

![image-20200411183705363](D:\test\git\crm\readme.assets\image-20200411183705363.png)

###  8、缓存管理

![image-20200411183831949](D:\test\git\crm\readme.assets\image-20200411183831949.png)

###  9、区域配置

主页面：

![image-20200411183906414](D:\test\git\crm\readme.assets\image-20200411183906414.png)

编辑页面：

![image-20200411183938301](D:\test\git\crm\readme.assets\image-20200411183938301.png)

###  10、主数据配置

主题域配置：

![image-20200411184056383](D:\test\git\crm\readme.assets\image-20200411184056383.png)

系统类配置：

![image-20200411184130641](D:\test\git\crm\readme.assets\image-20200411184130641.png)

属性配置：

![image-20200411184430628](D:\test\git\crm\readme.assets\image-20200411184430628.png)

属性值配置：

![image-20200411184548075](D:\test\git\crm\readme.assets\image-20200411184548075.png)

