# —*- coding:utf-8 -*-
# 编写接口测试用例
import unittest
import requests
import os, sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from db_fixture import test_data

class AddEventTest(unittest.TestCase):
	# 添加发布会
	def setUp(self):
		self.base_url = "http://127.0.0.1:8000/api/add_event/"

	def tearDown(self):
		print(self.result)

	def test_add_event_all_null(self):
		# 所有参数为空
		payload = {'eid':'','':'', 'limit':'', 'address':'', 'start_time':''}
		r = requests.post(self.base_url, data=payload)
		self.result = r.json()
		self.assertEqual(self.result['status'], 10021)
		self.assertEqual(self.result['message'], 'parameter error')

	def test_add_evnet_eid_exist(self):
		# id 已经存在
		payload = {'eid': 1, 'name': '一加4发布会', 'limit': 2000
				,'address': '深圳西乡', 'start_time': '2017'}
		r = requests.post(self.base_url, data=payload)
		self.result = r.json()
		self.assertEqual(self.result['status'], 10022)
		self.assertEqual(self.result['message'], 'event id already exists')

	def test_add_event_name_exist(self):
		# 名称已经存在
		payload = {'eid': 11, 'name': '红米 Pro 发布会', 'limit': 2000,
				'address': '北京水立方', 'start_time':'2017'}
		r = requests.post(self.base_url, data=payload)
		self.result = r.json()
		self.assertEqual(self.result['status'], 10023)
		self.assertEqual(self.result['message'], 'event name already exists')

	def test_add_event_data_type_error(self):
		# 日期格式错误
		payload = {'eid': 11,'name': '一加4手机发布会', 'limit':2000,
				'address':'北京水立方', 'start_time': '2017'}
		r = requests.post(self.base_url, data=payload)
		self.result = r.json()
		self.assertEqual(self.result['status'], 10024)
		error = 'start_time format error. It must be in YYYY-MM-DD HH:MM:SS format.'
		self.assertEqual(self.result['message'], error)

	def test_add_event_success(self):
		# 添加成功
		payload = {'eid':11, 'name':"一加手机发布会", 'limit':2000,
				   'address':'北京水立方','start_time':'2017-02-09 14:00:00'}
		r = requests.post(self.base_url, data=payload)
		self.result = r.json()
		self.assertEqual(self.result['status'], 200)
		self.assertEqual(self.result['message'], 'add event success')

if __name__ == "__main__":
	test_data.init_data() # 初始化接口测试数据
	unittest.main()