# 产品表
CREATE TABLE `b_thing` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) DEFAULT NULL,
  `cover` varchar(100) DEFAULT NULL,
  `description` longtext,
  `price` varchar(50) DEFAULT NULL,
  `status` varchar(1) NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `recommend_count` int(11) NOT NULL DEFAULT '0',
  `wish_count` int(11) NOT NULL DEFAULT '0',
  `collect_count` int(11) NOT NULL DEFAULT '0',
  `classification_id` bigint(20) DEFAULT NULL,
  `property` int(11) DEFAULT '0',
  `remark` varchar(255) DEFAULT NULL,
  `purchase` int(11) DEFAULT '0',
  `volume` float DEFAULT '0',
  `sku` varchar(100) DEFAULT NULL,
  `length` float DEFAULT NULL,
  `width` float DEFAULT NULL,
  `height` float DEFAULT NULL,
  `packing_quantity` int(11) DEFAULT NULL,
  `freight` float DEFAULT NULL,
  `value_added_tax` float DEFAULT NULL,
  `tariff` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sku` (`sku`),
  KEY `b_thing_classification_id_47675ac4_fk_b_classification_id` (`classification_id`),
  CONSTRAINT `b_thing_classification_id_47675ac4_fk_b_classification_id` FOREIGN KEY (`classification_id`) REFERENCES `b_classification` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=290 DEFAULT CHARSET=utf8


CREATE TABLE `b_finance` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `remark` varchar(100) DEFAULT NULL,
  `type` varchar(1) NOT NULL,
  `create_time` datetime(6) DEFAULT NULL,
  `money` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8


# 订单表
# status 0: 运输中
CREATE TABLE `b_order` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `sku` varchar(100) DEFAULT '',
  `status` varchar(2) DEFAULT '0',
  `order_amount` decimal(10,2) NOT NULL,
  `order_time` datetime(6) DEFAULT NULL,
  `shipment_time` datetime(6) DEFAULT NULL,
  `sign_time` datetime(6) DEFAULT NULL,
  `thing_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `count` int(11) NOT NULL,
  `order_number` varchar(100) DEFAULT NULL,
  `remark` varchar(30) DEFAULT NULL,
  `store_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_sku` (`order_number`,`sku`),
  KEY `fk_b_order_b_thing` (`sku`),
  CONSTRAINT `fk_b_order_b_thing` FOREIGN KEY (`sku`) REFERENCES `b_thing` (`sku`)
) ENGINE=InnoDB AUTO_INCREMENT=439 DEFAULT CHARSET=utf8

# 退款表
CREATE TABLE `b_refund` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `order_number` varchar(100) NOT NULL,
  `sku` varchar(100) NOT NULL,
  `refund_amount` decimal(10,2) NOT NULL,
  `refund_reason` varchar(255) NOT NULL,
  `refund_date` datetime NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_refund_order` (`order_number`),
  KEY `fk_refund_sku` (`sku`),
  CONSTRAINT `fk_refund_order` FOREIGN KEY (`order_number`) REFERENCES `b_order` (`order_number`),
  CONSTRAINT `fk_refund_sku` FOREIGN KEY (`sku`) REFERENCES `b_thing` (`sku`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8


#
CREATE TABLE ozon_cost (
    id INT AUTO_INCREMENT PRIMARY KEY,
    store_name VARCHAR(100),
    cost_type VARCHAR(2) DEFAULT '-1',
    day DATE NOT NULL,
    cost DECIMAL(10,2) DEFAULT NULL
);

ALTER TABLE ozon_cost
ADD CONSTRAINT unique_store_day_cost UNIQUE (store_name, day,cost_type);


# 销售额
CREATE TABLE ozon_sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    store_name VARCHAR(100),
    accruals_for_sale DECIMAL(10, 2),
    sale_commission DECIMAL(10, 2),
    amount DECIMAL(10, 2),
    type VARCHAR(50)
    day DATE NOT NULL,
);

# 数据分析
CREATE TABLE `b_seller_metrics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `day` date NOT NULL,
  `store_name` varchar(100) NOT NULL,
  `revenue` decimal(10,2) DEFAULT NULL,
  `ordered_units` int(11) DEFAULT NULL,
  `hits_view_search` int(11) DEFAULT NULL,
  `hits_view_pdp` int(11) DEFAULT NULL,
  `hits_view` int(11) DEFAULT NULL,
  `hits_tocart_search` int(11) DEFAULT NULL,
  `hits_tocart_pdp` int(11) DEFAULT NULL,
  `hits_tocart` int(11) DEFAULT NULL,
  `session_view_search` int(11) DEFAULT NULL,
  `session_view_pdp` int(11) DEFAULT NULL,
  `session_view` int(11) DEFAULT NULL,
  `conv_tocart_search` int(11) DEFAULT NULL,
  `conv_tocart_pdp` decimal(10,2) DEFAULT NULL,
  `conv_tocart` decimal(10,2) DEFAULT NULL,
  `returns` int(11) DEFAULT NULL,
  `cancellations` int(11) DEFAULT NULL,
  `delivered_units` int(11) DEFAULT NULL,
  `position_category` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_sku_day` (`store_name`, `day`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


# 退款排行视图
CREATE VIEW v_order_refund_rank AS
SELECT sku, SUM(count) AS count, SUM(order_amount) AS amount
FROM b_order
WHERE status = 2
GROUP BY sku;

SELECT sku, count, amount FROM v_order_refund_rank ORDER BY count;

# ozon 账单表
CREATE TABLE profit_statement (
    store_name VARCHAR(100) NOT NULL,  -- 店铺名称
    period VARCHAR(20) NOT NULL,  -- 时间段
    commission_amount DECIMAL(10, 2) NOT NULL,  -- 佣金
    item_delivery_and_return_amount DECIMAL(10, 2) NOT NULL,  -- 运输费
    orders_amount DECIMAL(10, 2) NOT NULL,  -- 签收
    returns_amount DECIMAL(10, 2) NOT NULL,  -- 退货
    services_amount DECIMAL(10, 2) NOT NULL,  -- 服务费
    return_commission DECIMAL(10, 2) NOT NULL,  -- 提现手续费
    cost DECIMAL(10, 2) NOT NULL,  -- 成本
    profit DECIMAL(10, 2) NOT NULL,  -- 利润
    PRIMARY KEY (store_name, period)  -- 联合主键
);