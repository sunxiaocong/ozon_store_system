from django.db import models


class User(models.Model):
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
    )
    ROLE_CHOICES = (
        ('0', '管理员'),
        ('1', '普通用户'),
    )
    STATUS_CHOICES = (
        ('0', '正常'),
        ('1', '封号'),
    )
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=50, null=True)
    role = models.CharField(max_length=2, blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')
    nickname = models.CharField(blank=True, null=True, max_length=20)
    avatar = models.FileField(upload_to='avatar/', null=True)
    mobile = models.CharField(max_length=13, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    description = models.TextField(max_length=200, null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    score = models.IntegerField(default=0, blank=True, null=True)
    push_email = models.CharField(max_length=40, blank=True, null=True)
    push_switch = models.BooleanField(blank=True, null=True, default=False)
    admin_token = models.CharField(max_length=32, blank=True, null=True)
    token = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        db_table = "b_user"


class Tag(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "b_tag"


class Classification(models.Model):
    list_display = ("title", "id")
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "b_classification"


class Thing(models.Model):
    STATUS_CHOICES = (
        ('0', '上架'),
        ('1', '下架'),
    )
    id = models.BigAutoField(primary_key=True)
    sku = models.CharField(max_length=100, unique=True)

    classification = models.ForeignKey(Classification, on_delete=models.CASCADE, blank=True, null=True,
                                       related_name='classification_thing')
    tag = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=30, blank=True, null=True)
    property = models.CharField(max_length=30, blank=True, null=True)  # 库存
    price = models.CharField(max_length=30, blank=True, null=True)
    remark = models.CharField(max_length=30, blank=True, null=True)
    cover = models.ImageField(upload_to='cover/', null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    purchase = models.CharField(max_length=30, default='0')  # 进货数
    volume = models.FloatField(default=0)
    length = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    packing_quantity = models.IntegerField(null=True, blank=True)
    freight = models.FloatField(null=True, blank=True)  # 运费
    value_added_tax = models.FloatField(null=True, blank=True)  # 增值税
    tariff = models.FloatField(null=True, blank=True)  # 关税
    shelf_cost = models.FloatField(null=True, blank=True)  # 上架费用
    weight = models.FloatField(null=True, blank=True)  # 重量
    all_cost = models.FloatField(default=0)
    low_tariff_price = models.FloatField(default=0)  # 最低报关金额

    class Meta:
        db_table = "b_thing"


class Finance(models.Model):
    STATUS_CHOICES = (
        ('0', '收入'),
        ('1', '支出'),
    )
    id = models.BigAutoField(primary_key=True)
    money = models.CharField(max_length=30, blank=True, null=True)
    remark = models.CharField(max_length=30, blank=True, null=True)
    type = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0')
    create_time = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "b_finance"


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    content = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_comment')
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE, null=True, related_name='thing_comment')
    comment_time = models.DateTimeField(auto_now_add=True, null=True)
    like_count = models.IntegerField(default=0)

    class Meta:
        db_table = "b_comment"


class Record(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_record')
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE, null=True, related_name='thing_record')
    title = models.CharField(max_length=100, blank=True, null=True)
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE, null=True,
                                       related_name='classification')
    record_time = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "b_record"


class LoginLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    ip = models.CharField(max_length=100, blank=True, null=True)
    ua = models.CharField(max_length=200, blank=True, null=True)
    log_time = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "b_login_log"


class OpLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    re_ip = models.CharField(max_length=100, blank=True, null=True)
    re_time = models.DateTimeField(auto_now_add=True, null=True)
    re_url = models.CharField(max_length=200, blank=True, null=True)
    re_method = models.CharField(max_length=10, blank=True, null=True)
    re_content = models.CharField(max_length=200, blank=True, null=True)
    access_time = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = "b_op_log"


class ErrorLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    ip = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    method = models.CharField(max_length=10, blank=True, null=True)
    content = models.CharField(max_length=200, blank=True, null=True)
    log_time = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "b_error_log"


class Banner(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.ImageField(upload_to='banner/', null=True)
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE, null=True, related_name='thing_banner')
    create_time = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "b_banner"


class Ad(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.ImageField(upload_to='ad/', null=True)
    link = models.CharField(max_length=500, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "b_ad"


class Notice(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.CharField(max_length=1000, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "b_notice"


class Address(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_address')
    name = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=30, blank=True, null=True)
    desc = models.CharField(max_length=300, blank=True, null=True)
    default = models.BooleanField(blank=True, null=True, default=False)  # 是否默认地址
    create_time = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "b_address"


# delivered 签收 cancelled 退货中 delivering 运输中
class Order(models.Model):
    STATUS_CHOICES = (
        ('0', '运输中'),
        ('1', '已签收'),
        ('2', '退货中'),
        ('99', '退货重新上架'),
    )
    id = models.BigAutoField(primary_key=True)
    sku = models.CharField(max_length=100, default='')
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='0')
    order_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_time = models.DateTimeField(null=True)  # 订单创建时间
    shipment_time = models.DateTimeField(null=True)  # 发运时间
    sign_time = models.DateTimeField(null=True)  # 签收时间
    thing_id = models.BigIntegerField(null=True)
    user_id = models.BigIntegerField(null=True)
    count = models.IntegerField()
    order_number = models.CharField(max_length=100, null=True)
    remark = models.CharField(max_length=30, null=True)
    store_name = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'b_order'
        unique_together = (('order_number', 'sku'),)


class OzonCost(models.Model):
    STATUS_CHOICES = (
        ('0', '模版'),
        ('1', '搜索'),
        ('2', '评论积分'),
        ('3', '超级卖家'),
        ('4', '仓库安置费'),
    )
    id = models.BigAutoField(primary_key=True)
    store_name = models.CharField(max_length=100)
    cost_type = models.CharField(max_length=2, choices=STATUS_CHOICES, default='-1')
    day = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'ozon_cost'
        unique_together = ('store_name', 'day', 'cost_type')


# 退货排行榜
class RefundRank(models.Model):
    sku = models.CharField(max_length=100, primary_key=True)
    count = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'v_order_refund_rank'


# 利润表
class ProfitStatement(models.Model):
    id = models.AutoField(primary_key=True)  # 自增主键
    store_name = models.CharField(max_length=100)
    period = models.CharField(max_length=30)
    commission_amount = models.CharField(max_length=30)
    item_delivery_and_return_amount = models.CharField(max_length=30)
    orders_amount = models.CharField(max_length=30)
    returns_amount = models.CharField(max_length=30)
    services_amount = models.CharField(max_length=30)
    return_commission = models.CharField(max_length=30)
    cost = models.CharField(max_length=30)
    profit = models.CharField(max_length=30)

    class Meta:
        managed = False  # 不以id为主键
        unique_together = (('store_name', 'period'),)  # 联合主键
        db_table = 'profit_statement'
