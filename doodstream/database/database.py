import datetime
import motor.motor_asyncio


class Database:
    
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
    
    
    def new_user(self, id):
        return dict(
            id = id,
            join_date = datetime.date.today().isoformat(),
            bot_updates=True,
            credential='',
            ban_status={
                'is_banned':False,
                'ban_duration':0,
                'banned_on':datetime.date.max.isoformat(),
                'ban_reason':''
            }
        )
    

################## Checking & Adding New User 👤 ##################

    async def is_user_exist(self, id):
        user = await self.col.find_one({'id':id})
        return True if user else False


    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)


################## Settings ⚙ ##################

    async def get_settings_status(self, id):
        user = await self.col.find_one({'id':id})
        return user.get('bot_updates', True)

    async def update_settings_status(self, id, value):
        await self.col.update_one({'id': id}, {'$set': {'bot_updates': value}})   


################## Google Credentials ##################

    async def get_credential_status(self, id):
        user = await self.col.find_one({'id':id})
        if not user:
            user = self.new_user(id)
            await self.col.insert_one(user)
        credentials = user.get('credential', '')
        return credentials

    async def update_credential_status(self, id, value):
        await self.col.update_one({'id': id}, {'$set': {'credential': value}})   



################## Ban Status 🚫 ##################

    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason=''
        )
        user = await self.col.find_one({'id':int(id)})
        return user.get('ban_status', default)

    async def ban_user(self, user_id, ban_duration, ban_reason):
        ban_status = dict(
            is_banned=True,
            ban_duration=ban_duration,
            banned_on=datetime.date.today().isoformat(),
            ban_reason=ban_reason
        )
        await self.col.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})

    async def remove_ban(self, id):
        ban_status = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason=''
        )
        await self.col.update_one({'id': id}, {'$set': {'ban_status': ban_status}})

    async def get_all_banned_users(self):
        banned_users = self.col.find({'ban_status.is_banned': True})
        return banned_users

    async def get_user_update(self):
         user = self.col.find({'updates': True})
         return user

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})


#################### THE END 🌋 #####################
