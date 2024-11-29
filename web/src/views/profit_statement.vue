<template>
  <div>
    <!--页面区域-->
    <div class="page-view">
      <div class="table-operations">
        <a-space style="width: 100%;display:flex;justify-content:space-between;">
          <div style="display:flex;">
            <a-range-picker format="YYYY-MM-DD HH:mm:ss" @change="onTimeChange"/>
            <a-input-search addon-before="店铺" enter-button @search="onSearch" @change="onSearchChange"/>
          </div>
        </a-space>
      </div>
      <a-table
          size="middle"
          rowKey="id"
          :loading="data.loading"
          :columns="columns"
          :data-source="data.dataList"
          :scroll="{ x: 'max-content' }"
          :pagination="{
          size: 'default',
          current: data.page,
          pageSize: data.pageSize,
          onChange: (current) => (data.page = current),
          showSizeChanger: false,
          showTotal: (total) => `共${total}条数据`,
        }"
      >
      </a-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import {listApi,} from '/@/api/ps';

const columns = reactive([
  {
    title: '周期',
    dataIndex: 'period',
    key: 'period',
  },
  {
    title: '店铺',
    dataIndex: 'store_name',
    key: 'store_name'
  },
  {
    title: '签收',
    dataIndex: 'orders_amount',
    key: 'orders_amount',
  },
  {
    title: '佣金',
    dataIndex: 'commission_amount',
    key: 'commission_amount'
  },
  {
    title: '运费',
    dataIndex: 'item_delivery_and_return_amount',
    key: 'item_delivery_and_return_amount'
  },
  {
    title: '退货',
    dataIndex: 'returns_amount',
    key: 'returns_amount',
  },
  {
    title: '服务费',
    dataIndex: 'services_amount',
    key: 'services_amount',
  },
  {
    title: '提现(签收12%)',
    dataIndex: 'return_commission',
    key: 'return_commission',
  },
  {
    title: '成本(签收30%)',
    dataIndex: 'cost',
    key: 'cost',
  },
  {
    title: '利润',
    dataIndex: 'profit',
    key: 'profit',
  }
]);


// 页面数据
const data = reactive({
  dataList: [],
  loading: false,
  keyword: '',
  selectedRowKeys: [] as any[],
  pageSize: 10,
  page: 1,
});


function onTimeChange(date, dateString) {
  console.log(date, dateString);
  getDataList(dateString[0], dateString[1]);
}

onMounted(() => {
  getDataList();
});

const getDataList = (start_time = '', end_time = '') => {
  data.loading = true;
  listApi({
    keyword: data.keyword,
    start_time,
    end_time,
  })
      .then((res) => {
        data.loading = false;
        console.log(res);
        res.data.forEach((item: any, index: any) => {
          item.index = index + 1;
        });
        data.dataList = res.data;
      })
      .catch((err) => {
        data.loading = false;
        console.log(err);
      });
}


const onSearchChange = (e: Event) => {
  data.keyword = e?.target?.value;
  console.log(data.keyword);
};

const onSearch = () => {
  getDataList();
};

</script>

<style scoped lang="less">
.page-view {
  min-height: 100%;
  background: #fff;
  padding: 24px;
  display: flex;
  flex-direction: column;
}

.table-operations {
  margin-bottom: 16px;
  text-align: right;
}

.table-operations > button {
  margin-right: 8px;
}
</style>
