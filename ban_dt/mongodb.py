import pymongo
import dns
import django
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
import os
from bson.objectid import ObjectId

from do_an_thuc_tap.settings import MONGO_KEY as url
os.environ['DJANGO_SETTINGS_MODULE'] = 'do_an_thuc_tap.settings'
django.setup()
from django.contrib.auth.models import User


database = pymongo.MongoClient(url).Project


def user_isExist(userId):
    try: User.objects.get(pk = userId)
    except User.DoesNotExist: return False
    else: return True


class ThuongHieu:
    collection = database.SanPham

    @staticmethod
    def all() -> list:
        query = ThuongHieu.collection.find({}, {'ThuongHieu': 1})
        return list(set([thuongHieu['ThuongHieu'] for thuongHieu in query]))


class SanPham:
    collection = database.SanPham

    # @staticmethod
    # def search(name):


    @staticmethod
    def is_exist(_id) -> bool:
        if SanPham.collection.find_one({"_id": ObjectId(_id)}):
            return True
        return False

    @staticmethod
    def chiTiet(_id : str):
        if result := SanPham.collection.find_one({'_id': ObjectId(_id)}):
            result['_id'] = str(result['_id'])
            return result
        return False

    @staticmethod
    def get_with_ThuongHieu(thuongHieu : str) -> list:
        result = list()
        for sanPham in SanPham.collection.find({'ThuongHieu': thuongHieu}):
            sanPham['_id'] = str(sanPham['_id'])
            result.append(sanPham)
        return result

    @staticmethod
    def newest() -> list:
        documents = SanPham.collection.find(
            {},
            {'_id': 1, 'ten': 1, 'mau': 1, 'anh': 1, 'cau hinh': 1}
        ).sort('nam', pymongo.DESCENDING).limit(10)
        return [
            {
                'id': str(document['_id']),
                'anh': str(document['mau'][0]['url']).replace(' ', '%20'),
                'ten': f"{document['ten']} - {document['cau hinh'][0]['rom']} {'GB' if document['cau hinh'][0]['rom'] !=1 else 'TB'}",
                'gia': document['cau hinh'][0]['price']
            } for document in documents
        ]


class GioHang:
    collection = database.GioHang

    @staticmethod
    def search(userId):
        if not user_isExist(userId): return False
        try:
            result = GioHang.collection.find_one({'userId': int(userId)})
        except ValueError:
            return False
        else:
            if result: return result
            return False

    # @staticmethod
    # def filter(filter : dict):
    #     return GioHang.collection.find(filter)

    @staticmethod
    def add(userId, sanPhamId):
        """Thêm sản phẩm vào giỏ hàng"""
        if not SanPham.is_exist(sanPhamId) and not user_isExist(userId): return False

        if gioHang:= GioHang.search(userId):
            chiTiet : list = gioHang['chi tiet']
            if len(chiTiet) == 0:
                GioHang.collection.insert_one({
                    'userId': userId,
                    'chi tiet': [
                        {
                            'sanPhamId': sanPhamId,
                            'so luong': 1
                        }
                    ]
                })
                return True
            for sanPham in chiTiet:
                if sanPham['sanPhamId'] == sanPhamId:
                    sanPham['so luong'] += 1
                    GioHang.collection.update_one({'_id': gioHang['_id']}, {'$set': {'chi tiet': chiTiet.append(sanPham)}})
                    return True
                if chiTiet.index(sanPham) + 1 == len(chiTiet):
                    sanPham = {
                        'sanPhamId': sanPhamId,
                        'so luong': 1
                    }
                    GioHang.collection.update_one({'_id': gioHang['_id']}, {'$set': {'chi tiet': chiTiet.append(sanPham)}})
                    return True
        else:
            GioHang.collection.insert_one({
                'userId': userId,
                'chi tiet': [
                    {
                        'sanPhamId': sanPhamId,
                        'so luong': 1
                    }
                ]
            })

    @staticmethod
    def remove(userId, sanPhamId):
        """Xóa sản phẩm khỏi giỏ hàng"""
        if not SanPham.is_exist(sanPhamId) or not user_isExist(userId): return False

        if GioHang.search(userId):
            if gioHang := GioHang.collection.find_one({'userId': userId, 'chi tiet.sanPhamId': sanPhamId}):
                chiTiet : list = gioHang['chi tiet']
                for sanPham in chiTiet:
                    if sanPham['sanPhamId'] == sanPhamId:
                        if int(sanPham['so luong']) - 1 == 0:
                            chiTiet.remove(sanPham)
                            GioHang.collection.update_one(
                                {'_id': gioHang['_id']},
                                {'$set': {'chi tiet': chiTiet.append(sanPham)}}
                            )
                            return True
                        sanPham['so luong'] -= 1
                        GioHang.collection.update_one(
                            {'_id': gioHang['_id']},
                            {'$set': {'chi tiet': chiTiet.append(sanPham)}}
                        )
                        return True
            return True
        return False
