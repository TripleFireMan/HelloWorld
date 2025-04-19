from django.db import models
from django.utils.translation import gettext_lazy as _
from system.storage import ImageStorage
from datetime import datetime
from rest_framework import serializers
from logging import getLogger
from phonenumber_field.modelfields import PhoneNumberField
logger = getLogger('HelloWorld')
ChooseType = (
    ('1','做爱'),
    ('2','自慰'),
    ('3','梦遗')
)

GenderType = (
    ('1','男'),
    ('2','女')
)

ShootPlaceChoice = (
    (1, '内射'),
    (2, '胸部'),
    (3, '嘴里'),
    (4, '颜射'),
    (5, '背上'),
    (6, '肚皮'),
    (7, '其他'),
)

MeasureChooice = (
    (1,'避孕套'),
    (2,'吃药'),
    (3,'无防护措施'),
)


UPLOAD_TO = 'SportRecord/%Y/%m/%d'
SR_BASE_URL_MEDIA_PATH = 'https://triplefireman.com/media/'
SR_BASE_URL = 'https://triplefireman.com'
class SRUserProfile(models.Model):
    username = models.CharField(_("用户名"), max_length=50,default='',blank=True, null=True)
    password = models.CharField(_("密码"), max_length=50,default='', blank=True, null=True)
    mobile = models.CharField(_("手机号"), max_length=50, default='', blank=True, null=True)
    name = models.CharField(default='', max_length=50, verbose_name='姓名')
    avator = models.CharField(default='', max_length=255, verbose_name='头像')
    address = models.CharField(_("地址"), max_length=50,default='',blank=True, null=True)
    birthday = models.DateField(_("出生日期"),editable=True,auto_now=True)
    created = models.DateTimeField(_("创建日期"),default=datetime.now)
    updated = models.DateTimeField(_("更新时间"), auto_now=True)
    role = models.ManyToManyField("SRRole", verbose_name=_("角色"), default=None, blank=True, null=True)
    gender = models.CharField(_("性别"), max_length=50, choices= GenderType, default='',blank=True, null=True)
    status = models.BooleanField(_("是否禁用 0-禁用 1-正常"),default=True)
    remark =  models.CharField(_("备注"), max_length=50, blank=True, null=True)
    class Meta:
        verbose_name='用户信息'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
    
class SRUserProfileSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%Y-%m-%d',read_only=True)
    updated = serializers.DateTimeField(format='%Y-%m-%d',read_only=True)
    birthday = serializers.DateField(format='%Y-%m-%d',read_only=True)
    role = serializers.SerializerMethodField()
    roleList = serializers.SerializerMethodField()
    places = serializers.SerializerMethodField()
    gender_text = serializers.CharField(source='get_gender_display',read_only=True)
    def get_role(self,obj):
        rlst = list()
        for r in obj.role.all():
            rlst.append(r.name)
        return ','.join(rlst)
    def get_roleList(self,obj):
        rlst = list()
        for r in obj.role.all():
            rlst.append(SRRoleSerializer(r).data)
        return rlst
    
    def get_places(self,obj):
        return SRPlaceSerializer(obj.places.all(),many=True).data
    class  Meta:
        model = SRUserProfile
        fields = '__all__'
        # depth = 3

class SRRole(models.Model):
    name = models.CharField(_("角色名称"), max_length=50)
    code = models.CharField(_("角色权限字符串"), max_length=50)
    create_time = models.DateTimeField(_("创建时间"),  auto_now_add=True, blank=True, null=True)
    update_time = models.DateTimeField(_("更新时间"),  auto_now=True, blank=True, null=True)
    remark =  models.CharField(_("备注"), max_length=50, blank=True, null=True)
    menu = models.ManyToManyField("SRMenu", verbose_name=_("菜单"), default=None, blank=True, null=True,related_name='roles')
    class Meta:
        verbose_name = '角色'
        verbose_name_plural = '角色s'
    def __str__(self):
        return self.name

class SRRoleSerializer(serializers.ModelSerializer):
    menuStr = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S',read_only=True)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S',read_only=True)
    def get_menuStr(self, obj):
        if obj.menu is not None:
            return ','.join([m.name for m in obj.menu.all()])
            

    class Meta:
        model = SRRole
        fields = '__all__'

class SRMenu(models.Model):
    name = models.CharField(_("菜单名称"), max_length=50)
    icon = models.CharField(_("菜单图标"), max_length=50)
    parent_id = models.IntegerField(_("父菜单id"))
    order_num = models.IntegerField(_("显示顺序"))
    path = models.CharField(_("路由地址"), max_length=50)
    component = models.CharField(_("组件路径"), max_length=50, blank=True, null=True)
    menu_type = models.CharField(_("菜单类型（M 目录 C 菜单 F 按钮）"), max_length=50)
    perms = models.CharField(_("权限标示"), max_length=50, blank=True, null=True)
    create_time = models.DateTimeField(_("创建时间"),  auto_now_add=True, blank=True, null=True)
    update_time = models.DateTimeField(_("更新时间"),  auto_now_add=True, blank=True, null=True)
    remark =  models.CharField(_("备注"), max_length=50, blank=True, null=True)
    
    def __lt__(self,otherNum):
        return self.order_num < otherNum.order_num
    
    class Meta:
        verbose_name = _("菜单")
        verbose_name_plural = _("菜单")

    def __str__(self):
        return self.name
    
class SRMenuSerializer(serializers.ModelSerializer):
    children =  serializers.SerializerMethodField()
    def get_children(self,obj):
        if hasattr(obj,'children'):
            serializerMenulist:list[SRMenuSerializer2] = list() # type: ignore
            for menu in obj.children:
                serializerMenulist.append(SRMenuSerializer2(menu).data)
            return serializerMenulist
            
    class Meta:
        model = SRMenu
        fields = '__all__'

class SRMenuSerializer2(serializers.ModelSerializer):
    class Meta:
        model = SRMenu
        fields = '__all__'




class SRSportCategory(models.Model):
    name = models.CharField(_("名称"), max_length=50,blank=True, null=True)
    icon = models.FileField(_("图标"), upload_to=UPLOAD_TO, max_length=100,blank=True, null=True)
    class Meta:
        verbose_name = '运动类型'
        verbose_name_plural = '运动类型'
    def __str__(self):
        return self.name

class SRUserSportRecord(models.Model):
    name = models.CharField(_("行为名称"), max_length=50, blank=True, null=True)
    address = models.CharField(_("行为地点"), max_length=50, blank=True, null=True)
    place =  models.ForeignKey('SRPlace', related_name='records', on_delete=models.CASCADE,verbose_name='位置')
    duration = models.IntegerField(_("持续时间"), blank=True, null=True)
    type = models.CharField(_("类型"), max_length=50, choices=ChooseType,default='',blank=True, null=True)
    propertys = models.ManyToManyField("SRProperty", verbose_name=_("使用的道具"),blank=True, default = None, related_name='records')
    partner = models.ManyToManyField("SRPartner", verbose_name=_("伴侣"), blank=True, null=True, related_name='records')
    score = models.ForeignKey("SRScore", verbose_name=_("打分"), on_delete=models.SET_NULL,related_name='records',blank=True, null=True)
    mood = models.ForeignKey("SRMood", verbose_name=_("心情"), on_delete=models.SET_NULL, related_name='records',blank=True, null=True)
    remark = models.CharField(_("备注"), max_length=50, blank=True, null=True)
    measure = models.CharField(_("安全措施"),max_length=50, default='', choices=MeasureChooice, help_text='采取的安全措施，1-安全套，2-吃药,3-无保护措施')
    isSender = models.BooleanField(_("是否是发起方"), default=True)
    isHigh = models.BooleanField(_("是否潮吹"),default=False)
    highTime = models.SmallIntegerField(_("高潮次数"),default=0)
    highTimePartner = models.SmallIntegerField(_("伴侣高潮次数"),default=0)
    shootPlace = models.CharField(_("射精位置"),choices=ShootPlaceChoice, max_length=50, blank=True, null=True)
    clothings = models.ManyToManyField("SRClothing", verbose_name=_("服装"),related_name='records',default=None,blank=True, null=True)
    photos = models.ManyToManyField("SRPhoto", verbose_name=_("甜美一刻"),related_name='records',default=None,blank=True, null=True)
    class Meta:
        verbose_name = '记录'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
    
class SRUserSportRecordSerializer(serializers.ModelSerializer):
    # mood = SRMoodSerializer()
    # def get_mood(self,obj):
    #     return SRMoodSerializer(obj.mood).data
    class Meta:
        model =  SRUserSportRecord
        fields = '__all__'
        # depth = 1
    
class SRPartner(models.Model):
    name = models.CharField(_("昵称"), max_length=50,default='')
    birthday = models.DateField(_("生日"),default=datetime.now)
    gender = models.CharField(_("性别"), max_length=50,choices=GenderType,default='')
    mobile = PhoneNumberField(_("手机号"), max_length=50,default='', unique=True)
    avator = models.CharField(_("头像"), max_length=255,default='',error_messages={'required': '请选择头像'})
    remark = models.CharField(_("备注"), max_length=50,default='',blank=True, null=True)
    creater = models.ForeignKey(SRUserProfile, related_name='partners', on_delete=models.CASCADE,verbose_name='创建人',blank=True, null=True)
    class Meta:
        verbose_name = '伴侣'
        verbose_name_plural = '伴侣'
    def __str__(self):
        return self.name
class SRPartnerSerializer(serializers.ModelSerializer):
    birthday = serializers.CharField(read_only = True)
    gender_text = serializers.CharField(source='get_gender_display',read_only=True)
    mobile_text = serializers.SerializerMethodField()
    # creater = serializers.StringRelatedField()
    def get_mobile_text(self,obj):
        return obj.mobile.as_national
    class Meta:
        model = SRPartner
        fields = '__all__'
        depth = 1

class SRProperty(models.Model):
    name = models.CharField(_("名称"), max_length=50)
    icon = models.CharField(_("图标"),max_length=255,default='')
    bgColor = models.CharField(_("背景色"), max_length=50,blank=True, null=True, default= '')
    class Meta:
        verbose_name = '道具'
        verbose_name_plural = '道具'
    def __str__(self):
        return self.name
    
class SRPropertySerializier(serializers.ModelSerializer):
    class Meta:
        model = SRProperty
        fields = '__all__'

class SRClothing(models.Model):
    name = models.CharField(_("名称"), max_length=50)
    icon = models.CharField(_("图标"), max_length=255)    
    bgColor = models.CharField(_("背景色"), max_length=50,blank=True, null=True, default= '')
    class Meta:
        verbose_name = '服装'
        verbose_name_plural = '服装'
    def __str__(self):
        return self.name

class SRClothingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SRClothing
        fields = '__all__'
        
class SRSystemConfig(models.Model):
    name = models.CharField(_("应用名称"), max_length=50)
    isInReView = models.BooleanField(_("是否在审核"))
    class Meta:
        verbose_name = '系统配置接口'
        verbose_name_plural = '系统配置接口'
    def __str__(self):
        return self.name

class SRScore(models.Model):
    name = models.CharField(_("分数"), max_length=50, default = '',blank=True, null=True)
    score = models.SmallIntegerField(_("分数1-5"))
    icon = models.CharField(_("分数图标"), max_length=255,blank=True, null=True, default= '')
    class Meta:
        db_table = 'srscore'
        managed = True
        verbose_name = '分数'
        verbose_name_plural = '分数'
    def __str__(self):
        return str(self.score)

class SRMood(models.Model):
    name = models.CharField(_("心情"), max_length=50, default = '',blank=True, null=True)
    icon = models.CharField(_("心情图标"), max_length=255,blank=True, null=True, default= '')
    class Meta:
        db_table = 'srmood'
        managed = True
        verbose_name = '心情'
        verbose_name_plural = '心情'
    def __str__(self):
        return str(self.name)
    
class SRMoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = SRMood
        fields = '__all__'



class SRPhoto(models.Model):
    url = models.ImageField(_("图片"), upload_to=UPLOAD_TO, height_field=None, width_field=None, max_length=None)
    def __str__(self):
        return str(self.url)

    class Meta:
        verbose_name = '图片'
        verbose_name_plural = '图片'

class SRPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SRPhoto
        fields = '__all__'

PlaceChoice = (
    ('1','系统推荐'),
    ('2','用户添加'),
)

class SRPlace(models.Model):
    name = models.CharField(_("地点名称"), max_length=50)
    type = models.CharField(_("地点分类"), max_length=50, choices=PlaceChoice, blank=True, null=True) # admin 是默认类型，空值的话是用户自己添加的
    createTime = models.DateTimeField(_("创建时间"), auto_now_add=True, blank=True, null=True)
    uploadTime = models.DateTimeField(_("更新时间"), auto_now=True, blank=True, null=True)
    creater = models.ForeignKey(SRUserProfile, verbose_name=_("创建人"), on_delete=models.CASCADE, related_name='places')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '地点'
        verbose_name_plural = '地点s'
class SRPlaceSerializer(serializers.ModelSerializer):

    createTime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S',read_only=True)
    uploadTime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S',read_only=True)
    creater = serializers.StringRelatedField()
    
    class Meta:
        model = SRPlace
        fields = '__all__'