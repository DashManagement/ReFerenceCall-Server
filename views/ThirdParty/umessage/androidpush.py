'''
Description: 
Author: fanshaoqiang
Date: 2016-08-10 16:58:57
LastEditTime: 2021-07-27 12:08:13
LastEditors: fanshaoqiang
'''
'''
Description: 
Author: fanshaoqiang
Date: 2016-08-10 16:58:57
LastEditTime: 2021-07-02 12:00:06
LastEditors: fanshaoqiang
'''




from views.ThirdParty.umessage.androidnotification import AndroidNotification
from views.ThirdParty.umessage.umengnotification import MsgType
class AndroidUnicast(AndroidNotification):

    def __init__(self,
                 appKey,
                 appMasterSecret,
                 ):
        AndroidNotification.__init__(self, appKey, appMasterSecret)
        self.setPredefinedKeyValue(self.CONSTR_TYPE, MsgType.uniCast)

    def setDeviceToken(self, token):
        self.setPredefinedKeyValue("device_tokens", token)


class AndroidListcast(AndroidNotification):

    def __init__(self,
                 appKey,
                 appMasterSecret,
                 ):
        AndroidNotification.__init__(self, appKey, appMasterSecret)
        self.setPredefinedKeyValue(self.CONSTR_TYPE, MsgType.listCast)

    def setDeviceToken(self, token):
        self.setPredefinedKeyValue("device_tokens", token)


class AndroidGroupcast(AndroidNotification):

    def __init__(self,
                 appKey,
                 appMasterSecret,
                 ):
        AndroidNotification.__init__(self, appKey, appMasterSecret)
        self.setPredefinedKeyValue(self.CONSTR_TYPE, MsgType.groupCast)

    def setFilter(self, filter):
        self.setPredefinedKeyValue("filter", filter)


class AndroidFilecast(AndroidNotification):

    def __init__(self,
                 appKey,
                 appMasterSecret,
                 ):
        AndroidNotification.__init__(self, appKey, appMasterSecret)
        self.setPredefinedKeyValue(self.CONSTR_TYPE, MsgType.fileCast)

    def setFileId(self, fileId):
        self.setPredefinedKeyValue("file_id", fileId)


class AndroidCustomizedcast(AndroidNotification):

    def __init__(self,
                 appKey,
                 appMasterSecret,
                 ):
        AndroidNotification.__init__(self, appKey, appMasterSecret)
        self.setPredefinedKeyValue(self.CONSTR_TYPE, MsgType.customizedCast)

    def setAlias(self, alias, aliasType):
        self.setPredefinedKeyValue("alias", alias)
        self.setPredefinedKeyValue("alias_type", aliasType)

    def setFileId(self, fileId, aliasType):
        self.setPredefinedKeyValue("file_id", fileId)
        self.setPredefinedKeyValue("alias_type", aliasType)


class AndroidBroadcast(AndroidNotification):

    def __init__(self,
                 appKey,
                 appMasterSecret,
                 ):
        AndroidNotification.__init__(self, appKey, appMasterSecret)
        self.setPredefinedKeyValue(self.CONSTR_TYPE, MsgType.broadCast)
