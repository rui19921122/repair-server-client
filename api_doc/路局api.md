# 路局天窗修计划查询 #


## 一、 网址  ##
[http://10.128.20.156:8080/tcx/](http://10.128.20.156:8080/tcx/ "天窗修计划网址") 

## 二、 爬取的内容 

> 注： 此网站查询的内容无需登录

### 2.1 查询天窗修历史开放计划

1. 请求链接
	> http://host.com/scrapy-plan/repair/
2. 请求方法
	> GET
3. 请求参数

	开始日期 start_date: 格式为 YYYY-MM-DD
	
	结束日期 end_date: 格式为 YYYY-MM-DD

	强制刷新(可选） force_update: 值为true|false, 默认为false

	>如果选择了这个参数，则强制从路局网站强制爬取，不考虑缓存

4. 返回内容格式
	> ScrapyPlanInterface

		{
			length:number, # 长度
			data: # 数据
				{
					number : string; 					# 编号，格式为4位数字
					post_date : date; 					# 日期，格式为YYYY-MM-DD
					type: string; 						# 类型，值为I、II、站控
					direction: "上行"|"下行"|"单线"; 		# 行别
					area: string;						# 维修区域
					plan_time: string；					# 计划时间，值格式为hh:mm-hh:mm或者单纯的字符串
					apply_place : string;				# 作业申请站
					content:							# 工作内容
						{
							work_department : string;		# 作业单位
							work_place : string;			# 作业地点
							work_project : string;			# 作业项目
							work_detail : string;			# 作业明细
							off_power_unit: string[];		# 停电单元
							work_vehicle: string;			# 作业车配合
							protect_mileage: string;		# 防护里程
							on_duty_person: string[];		# 负责人
							operate_track_switch: boolean;	# 是否搬动道岔
							work_with_department : string[];	# 配合单位
							extra_message: string;			# 补充作业事项
						}[]
				}[]
		}
		
	
### 2.2 查询电务垂停历史计划

	> 由于查询网站返回的数据不包含日期，因此无法应用。

# 路局天窗修历史查询（电子登销记系统）

## 1. 网址 
[http://10.128.20.119:8080/dzdxj/login.faces](http://10.128.20.119:8080/dzdxj/login.faces "路局天窗修历史查询")

## 2. 爬取的内容
### 2.1 查询天窗修历史实绩

1. 请求链接
	> http://host.com/scrapy-history/repair/
2. 请求方法
	> GET
3. 请求参数

	开始日期 start_date: 格式为 YYYY-MM-DD
	
	结束日期 end_date: 格式为 YYYY-MM-DD

	强制刷新(可选） force_update: 值为true|false, 默认为false

	>如果选择了这个参数，则强制从路局网站强制爬取，不考虑缓存

4. 返回内容格式
	> ScrapyHistoryInterface

		{
			length:number, # 长度
			data: # 数据
				{
					plan_type: string; 					# 计划类型，值为普(V型)、普(站控)等
					number : string;

					# 维修计划号，格式为YYYYMMDD-[DZJ]\d{3,4},[DZJ]指的是电务垂直，站控，局控，3-4位数字为计划号
	
					date : date; 						# 维修日期，格式为YYYYMMDD
					plan_time: string；					# 维修时间，值格式为hh:mm-hh:mm或者单纯的字符串
					repair_content : string 			# 维修项目
					repair_department : string[];		# 维修主体单位
					apply_place : string;				# 登记站，即作业申请站
					inner_id : string;					# 存储在路局内的系统ID，用于查询详细信息
					use_paper : boolean: 				# 是否采用纸质登记
		}

### 2.2 查询天窗修历史实绩详细信息

1. 请求链接
	> http://host.com/scrapy-history/repair/(\d{6})/
	> 
	> 6位数字唯一对应了相关信息
2. 请求方法
	> GET
3. 请求参数

	强制刷新(可选） force_update: 值为true|false, 默认为false

	>如果选择了这个参数，则强制从路局网站强制爬取，不考虑缓存

4. 返回内容格式
	> ScrapyHistoryDetailInterface

		{
			number:string;				#施工维修编号，格式为[JDZ]\d{3}
			repair_content: string;		#施工项目
			effect_area: string;		#影响使用范围
			publish_start_time: hh:mm	#命令号发布时间
			publish_start_number:string;	#开始施工命令号码
			actual_start_time: hh:mm;       #施工开始时间
			actual_end_time: hh:mm		#命令号结束时间
			actual_end_number: string;	#开通施工命令号码
			actual_host_person: string;	#把关人
			
		}