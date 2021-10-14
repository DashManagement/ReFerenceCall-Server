'''
@Description:
@Author: michael
@Date: 2021-08-05 10:16:20
LastEditTime: 2021-08-07 23:46:33
LastEditors: fanshaoqiang
'''

# coding=utf-8

# 加载自己创建的包
import pymongo
from views.Base import *
from config.log_config import logger

# meeting 我的/其它的 - 预约会议流程列表


class BookingMeetingList:

    id = ''
    request_type = ''
    check_type = ''
    data_num = ''
    query_field = ''

    def __init__(self):
        self.id=''
        self.request_type=''
        self.data_num=''
        self.check_type = ''
        self.data_num = ''

    # 返回我的/其它的 - 会议记录列表
    def construct(self, id='', request_type='', data_num=''):

        if id == "refid":
            return {
                "code": 200,
                "count": 0,
                "data": [],
                "message": "no login"
            }

        self.id = int(id)
        self.request_type = int(request_type)
        self.data_num = int(data_num)

        # 连接数远程据库
        self.client = pymongo.MongoClient("mongodb://dash:dashmima!@118.193.47.247:8088/dash_test")
        self.db = self.client.dash_test
        self.collection = self.db.dash_users
        # 连接本地数据库
        # self.client = pymongo.MongoClient("localhost", 27017)
        # self.db = self.client["dash_test"]

        # 查看请求者是否存在 - 1
        condition = {'id':self.id}
        field = {'_id':0}
        result = self.db.dash_users.find_one(condition, field)

        if result is None or len(result) == 0:
            return {'code': 201, 'message':'用户不存在'}

        # 验证请求类型是否合法
        if self.request_type != 1 and self.request_type != 2:
            return {'code': 202, 'message': '错误的请求类型'}

        # 设置请求字段类型
        if self.request_type == 1:
            '''设置请求的字段类型为，查询我的'''
            self.query_field = 'start_id'
        else:
            '''设置请求的字段类型为，查询其它的'''
            self.query_field = 'end_id'

        # 查看用户列表信息
        result = self.getMeetingList()
        data = {'code': 200, 'count': len(result), 'data': result}
        # logger.info(data)

        return data


    # 查询被拒绝的和未完成的预约列表
    def getMeetingList(self):

        # dbo.resetInitConfig('test', 'reservation_meeting')
        logger.info({'field': self.query_field, 'id': self.id, 'request_type': self.request_type})

        # 获取第一次发起请求的所有数据
        condition = {self.query_field: self.id, 'request_num': 1}
        field = {'session_id': 1, '_id': 0}

        result = list(self.db.dash_reservation_meeting.find(condition, field))

        # 如果没有记录则直接返回空的 list 列表
        if len(result) == 0:
            return []

        # 获取单个 session_id 的所有预约记录
        booking_meeting_list = []
        for value in result:
            condition = {'session_id': value['session_id']}
            field = {
                "id": 1,
                "reservation_company_id": 1,
                "reservation_company_name": 1,
                "reservation_company_icon": 1,
                "session_id": 1,
                "start_id": 1,
                "start_user_name": 1,
                "start_head_portrait": 1,
                # "start_working_fixed_year": 1,
                "start_company_name": 1,
                "start_company_icon": 1,
                "end_id": 1,
                "end_user_name": 1,
                "end_head_portrait": 1,
                # "end_working_fixed_year": 1,
                "end_company_name": 1,
                "end_company_icon": 1,
                # "meeting_pass": 1,
                # "national_area_code": 1,
                # "national_area_name": 1,
                # "meeting_time": 1,
                # "meeting_status": 1,
                "volunteer_reply_time": 1,
                "volunteer_reply_time": 1,
                "requester_agree_time": 1,
                "request_num": 1,
                "discuss_number": 1,
                "last_id": 1,
                "current_id": 1,
                "is_create_meeting": 1,
                "status": 1,
                "create_time": 1,
                "time_zone_number" : 1,
                "time_zone" : 1,
                "_id": 0
            }
            # sort = [('id', -1)]
            skip = 0
            num = 100
            session_id_record = list(self.db.dash_reservation_meeting.find(condition, field).sort("create_time", pymongo.DESCENDING).limit(num).skip(skip))

            # session_id_record = dbo.findSort(condition, field, sort, skip, num)
            # print(session_id_record)
            is_complete = False
            # 查看当前记录是否为未完成
            for value_two in session_id_record:

                # 判断如果是当前ID发起的首次请求，并且自己拒绝的，则直接跳过
                if value_two['is_create_meeting'] == 2 and self.id == value_two['start_id'] and self.id == value_two['current_id']:
                    is_complete = False
                    continue

                # 查看是否预约还未完成状态
                if value_two['status'] == 1:
                    is_complete = True
                    '''当前用户 self.id 为请求者的时候 回复的消息'''
                    if session_id_record[0]['start_id'] == self.id and session_id_record[0]['current_id'] == self.id and session_id_record[0]['request_num'] == 1:
                        session_id_record[0]['message'] = '等待志愿者回复'
                    if session_id_record[0]['start_id'] == self.id and session_id_record[0]['end_id'] != self.id and session_id_record[0]['request_num'] == 2 and session_id_record[0]['last_id'] == self.id:
                        session_id_record[0]['message'] = '请求者已回复，等待志愿者确认'
                    '''当前用户 self.id 为志愿者的时候 回复的消息'''
                    if session_id_record[0]['end_id'] == self.id and session_id_record[0]['start_id'] != self.id and session_id_record[0]['request_num'] == 1:
                        session_id_record[0]['message'] = '请求预约会议'
                    if session_id_record[0]['end_id'] == self.id and session_id_record[0]['start_id'] != self.id and session_id_record[0]['request_num'] == 2 and session_id_record[0]['last_id'] == self.id:
                        session_id_record[0]['message'] = '志愿者已回复，等待请求者确认'

                # 查看当前记录是否为被拒绝
                if value_two['is_create_meeting'] == 2:
                    '''当前用户 self.id 为请求者时候 拒绝的消息'''
                    if session_id_record[0]['start_id'] == self.id and session_id_record[0]['current_id'] != self.id and session_id_record[0]['request_num'] == 2:
                        session_id_record[0]['message'] = '志愿者拒绝参加会议'
                    '''当前用户 self.id 为志愿者的时候 拒绝的消息'''
                    if session_id_record[0]['end_id'] == self.id and session_id_record[0]['current_id'] == self.id and session_id_record[0]['request_num'] == 2:
                        session_id_record[0]['message'] = '您已拒绝的会议'
                    if session_id_record[0]['end_id'] == self.id and session_id_record[0]['start_id'] != self.id and session_id_record[0]['request_num'] == 3:
                        session_id_record[0]['message'] = '请求者拒绝参加会议'
                    is_complete = True

            if is_complete is True:
                booking_meeting_list.insert(0, session_id_record[0])

        # 添加用户的匿名字段到数据中
        for value in booking_meeting_list:

            if self.request_type == 1:
                search_user_id = value['end_id']

            if self.request_type == 2:
                search_user_id = value['start_id']

            condition = {'id': search_user_id}
            field = {'is_anonymous':1, '_id':0}
            result = self.db.dash_users.find_one(condition, field)

            if result is None or len(result) == 0:
                return {'code': 209, 'message':'用户是否匿名的属性不存在'}

            # 增加匿名属性字段
            value['is_anonymous'] = result['is_anonymous']


        return booking_meeting_list









# bookingMeetingList = BookingMeetingList()
