'''
@Description:
@Author: michael
@Date: 2021-08-08 10:16:20
LastEditTime: 2021-08-08 20:00:00
LastEditors: michael
'''

# coding=utf-8

# 加载自己创建的包
from views.Base import *
from views.reference_call_api.TimeOperation import timeOperation
from config.log_config import logger

# meeting 我的/其它的 - 预约会议流程列表
class MeetingSchedule:


    id = ''

    # 返回我的/其它的 - 会议记录列表
    async def construct(self, id=''):

        self.id = int(id)

        # 查看请求者是否存在
        user_info = await self.getUserInfo()
        if user_info is False:
            return {'code':201, 'message':'无效的用户id'}

        # 查看用户列表信息
        user_meeting_list = await self.getMeetingScheduleList(user_info)

        # 计算未来 N 天之内的会议日程
        return await self.futureSchedule(user_meeting_list)
        return user_meeting_list
        # return {'code':200, 'count':len(result), 'data':result}


    # 查询已经约定的会议日程接口
    async def getMeetingScheduleList(self, user_info):

        dbo.resetInitConfig('test', 'meeting_list')
        condition = {'status':1, 'meeting_status':0, '$or':[
            {'start_id':self.id},
            {'end_id':self.id}  
        ]}
        field = {
            "id": 1,
            "start_id": 1,
            "start_user_name": 1,
            "start_head_portrait": 1,
            "start_company_name": 1,
            "start_company_icon": 1,
            "end_id": 1,
            "end_user_name": 1,
            "end_head_portrait": 1,
            "end_company_name": 1,
            "end_company_icon": 1,
            "session_id": 1,
            "start_time": 1,
            "meeting_id": 1,
            "meeting_pass": 1,
            "meeting_address": 1,
            "meeting_time": 1,
            'create_time':1,
            '_id':0
        }
        result = await dbo.getData(condition, field)

        for value in result:
            value['name'] = user_info['name']
            value['company_name'] = user_info['company_name']

        return result


    # 计算未来 N 天之内的会议日程
    async def futureSchedule(self, user_meeting_list):
        '''
        :param user_meeting_list list 该用的会议信息列表
        '''

        schedult_list = []
        # 获取 N 天之内的 早9点 到 晚6点 的时间列表
        time_list = await timeOperation.returnTimeStamp(10)
        # 将未来 N 天的时候列表 与 会议时间匹配
        for value in time_list:
            tmp_schedult = []
            for value_two in user_meeting_list:
                # return value_two
                # logger.info(value)
                # logger.info(value_two)
                if int(value_two['meeting_time'][0]) >= int(value['time_stamp'][0]) and int(value_two['meeting_time'][1]) <= int(value['time_stamp'][1]):
                    tmp_schedult.append(value_two)

            # 如果有会议记录，则添加进列表中一段会议时间的详细信息
            if len(tmp_schedult) > 0:
                # print(len(tmp_schedult))
                # tmp_schedult['time_info'] = value['time_info']
                schedult_list.append(
                    {'time_info':value['time_info'], 'meeting':{'count':len(tmp_schedult), 'list':tmp_schedult}}
                )

        # 整理用户信息返回的字段
        result = await self.finishingReturnUserInfoField(schedult_list)

        data = {'code':200, 'data':{'count':len(result), 'schedult_list':result}}
        return data


    # 整理用户信息字段
    async def finishingReturnUserInfoField(self, schedult_list):

        for value in schedult_list:
            for meeting in value['meeting']['list']:
                if self.id == meeting['start_id']:
                    meeting['name'] = meeting['start_user_name']
                    meeting['head_portrait'] = meeting['start_head_portrait']
                    meeting['company_name'] = meeting['start_company_name']
                    meeting['company_icon'] = meeting['start_company_icon']
                if self.id == meeting['end_id']:
                    meeting['name'] = meeting['end_user_name']
                    meeting['head_portrait'] = meeting['end_head_portrait']
                    meeting['company_name'] = meeting['end_company_name']
                    meeting['company_icon'] = meeting['end_company_icon']

                del meeting['start_user_name'], meeting['start_head_portrait'], meeting['start_company_name'], meeting['start_company_icon']
                del meeting['end_user_name'], meeting['end_head_portrait'], meeting['end_company_name'], meeting['end_company_icon']

        return schedult_list


    # 获取用户信息
    async def getUserInfo(self):

        dbo.resetInitConfig('test','users')
        condition = {'id':self.id}
        field = {'_id':0}
        result = await dbo.findOne(condition, field)
        # logger.info(result)
        if result is None:
            return False

        return result









meetingSchedule = MeetingSchedule()