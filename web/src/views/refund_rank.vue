<template>
  <div>
    <!--页面区域-->
    <div class="page-view">
      <div class="table-operations">
        <a-space>
          <!-- 添加下拉框 -->
          <a-select placeholder="排序顺序" @change="onSelectChange" style="width: 200px;">
            <a-select-option value="return_rate">按退货率</a-select-option>
            <a-select-option value="1_count">按签收</a-select-option>
            <a-select-option value="0_count">按运输中</a-select-option>
          </a-select>
          <a-range-picker format="YYYY-MM-DD HH:mm:ss" @change="onTimeChange"/>
          <a-input-search addon-before="名称" enter-button @search="onSearch" @change="onSearchChange"/>
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
import {listApi} from '/@/api/refund_rank';

const columns = reactive([
  {
    title: 'SKU',
    dataIndex: 'sku',
    key: 'sku'
  },
  {
    title: '运输中数量',
    dataIndex: '0_count',
    key: '0_count'
  },
  {
    title: '签收数量',
    dataIndex: '1_count',
    key: '1_count'
  },
  {
    title: '退货数量',
    dataIndex: '2_count',
    key: '2_count'
  },
  {
    title: '退货率%',
    dataIndex: 'return_rate',
    key: 'return_rate'
  }
]);


// 页面数据
const data = reactive({
  dataList: [],
  loading: false,
  keyword: '',
  desc_key: '',
  start_time: '',
  end_time: '',
  selectedRowKeys: [] as any[],
  pageSize: 10,
  page: 1,
});


onMounted(() => {
  getDataList();
});

function onTimeChange(date, dateString) {
  console.log(date, dateString);
  data.start_time = dateString[0]
  data.end_time = dateString[1]
  console.log(data)
  getDataList();
}

function onSelectChange(value) {
  console.log('选择的值:', value);
  data.desc_key = value
  // 处理下拉框选择变化
  console.log(data)
  getDataList();
}


const getDataList = () => {
  data.loading = true;
  console.log(data)
  listApi({
    keyword: data.keyword,
    start_time: data.start_time,
    end_time: data.end_time,
    desc_key: data.desc_key,
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
