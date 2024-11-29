<template>
  <div class="page-view">
    <div class="table-operations">
      <a-space>
        <a-range-picker format="YYYY-MM-DD HH:mm:ss" @change="onTimeChange"/>
        <a-select
            v-model:value="storeIds"
            mode="multiple"
            style="width: 100%"
            placeholder="选择店铺"
            :options="selectOpt"
            @change="handleChange"
        ></a-select>
      </a-space>
    </div>
    <div class="table-container">
      <a-table :columns="columns" :data-source="data" row-key="key">
        <template #header>
          <a-space>
            <span>报告占比</span>
          </a-space>
        </template>
      </a-table>
    </div>
  </div>
</template>


<script setup lang="ts">
import {listApi} from "/@/api/store_ad";

const columns = ref([
  {
    title: "日期",
    dataIndex: "day",
    key: "day",
  },
  {
    title: "店铺001",
    children: [
      {
        title: "营业额",
        dataIndex: "a.revenue",
        key: "a.revenue",
        customRender: ({text, record, index, column}) => {
          return record.a.revenue;
        },
      },
      {
        title: "模版",
        dataIndex: "a.model_cost",
        key: "a.model_cost",
        customRender: ({text, record, index, column}) => {
          return record.a.model_cost;
        },
      },
      {
        title: "搜索",
        dataIndex: "a.search_cost",
        key: "a.search_cost",
        customRender: ({text, record, index, column}) => {
          return record.a.search_cost;
        },
      },
    ],
  },
  {
    title: "店铺002",
    children: [
      {
        title: "营业额",
        dataIndex: "b.revenue",
        key: "b.revenue",
        customRender: ({text, record, index, column}) => {
          return record.b.revenue;
        },
      },
      {
        title: "模版",
        dataIndex: "b.model_cost",
        key: "b.model_cost",
        customRender: ({text, record, index, column}) => {
          return record.b.model_cost;
        },
      },
      {
        title: "搜索",
        dataIndex: "b.search_cost",
        key: "b.search_cost",
        customRender: ({text, record, index, column}) => {
          return record.b.search_cost;
        },
      },
    ],
  },
  {
    title: "店铺003",
    children: [
      {
        title: "营业额",
        dataIndex: "c.revenue",
        key: "c.revenue",
        customRender: ({text, record, index, column}) => {
          return record.c.revenue;
        },
      },
      {
        title: "模版",
        dataIndex: "c.model_cost",
        key: "c.model_cost",
        customRender: ({text, record, index, column}) => {
          return record.c.model_cost;
        },
      },
      {
        title: "搜索",
        dataIndex: "c.search_cost",
        key: "c.search_cost",
        customRender: ({text, record, index, column}) => {
          return record.c.search_cost;
        },
      },
    ],
  },
  // {
  //   title: "店铺004",
  //   children: [
  //     {
  //       title: "营业额",
  //       dataIndex: "d.revenue",
  //       key: "d.revenue",
  //       customRender: ({text, record, index, column}) => {
  //         return record.d.revenue;
  //       },
  //     },
  //     {
  //       title: "橱板广告费",
  //       dataIndex: "d.model_cost",
  //       key: "d.model_cost",
  //       customRender: ({text, record, index, column}) => {
  //         return record.d.model_cost;
  //       },
  //     },
  //     {
  //       title: "搜索广告费",
  //       dataIndex: "d.search_cost",
  //       key: "d.search_cost",
  //       customRender: ({text, record, index, column}) => {
  //         return record.d.search_cost;
  //       },
  //     },
  //   ],
  // },
  // {
  //   title: "店铺005",
  //   children: [
  //     {
  //       title: "营业额",
  //       dataIndex: "e.revenue",
  //       key: "e.revenue",
  //       customRender: ({text, record, index, column}) => {
  //         return record.e.revenue;
  //       },
  //     },
  //     {
  //       title: "橱板广告费",
  //       dataIndex: "e.model_cost",
  //       key: "e.model_cost",
  //       customRender: ({text, record, index, column}) => {
  //         return record.e.model_cost;
  //       },
  //     },
  //     {
  //       title: "搜索广告费",
  //       dataIndex: "e.search_cost",
  //       key: "e.search_cost",
  //       customRender: ({text, record, index, column}) => {
  //         return record.e.search_cost;
  //       },
  //     },
  //   ],
  // },
  {
    title: "店铺006",
    children: [
      {
        title: "营业额",
        dataIndex: "f.revenue",
        key: "f.revenue",
        customRender: ({text, record, index, column}) => {
          return record.f.revenue;
        },
      },
      {
        title: "模版",
        dataIndex: "f.model_cost",
        key: "f.model_cost",
        customRender: ({text, record, index, column}) => {
          return record.f.model_cost;
        },
      },
      {
        title: "搜索",
        dataIndex: "f.search_cost",
        key: "f.search_cost",
        customRender: ({text, record, index, column}) => {
          return record.f.search_cost;
        },
      },
    ],
  },
  {
    title: "总店铺",
    children: [
      {
        title: "总营业额",
        dataIndex: "total_revenue",
        key: "total_revenue",
      },
      {
        title: "模版",
        dataIndex: "total_model_cost",
        key: "total_model_cost",
      },
      {
        title: "搜索",
        dataIndex: "total_search_cost",
        key: "total_search_cost",
      },
      {
        title: "模版占比",
        dataIndex: "model_cost_ratio",
        key: "model_cost_ratio",
      },
      {
        title: "搜索占比",
        dataIndex: "search_cost_ratio",
        key: "search_cost_ratio",
      },
    ],
  },
])
const data = ref([
  {
    key: 1,
    day: "2024-08-01",
    "a": {
      revenue: "8,064.00 ₽",
      model_cost: "454.75 ₽",
      search_cost: "1,135.30 ₽",
    },
    "b": {
      revenue: "42,642.00 ₽",
      model_cost: "8,989.82 ₽",
      search_cost: "1,839.60 ₽",
    },
    "c": {
      revenue: "42,642.00 ₽",
      model_cost: "8,989.82 ₽",
      search_cost: "1,839.60 ₽",
    },
    "d": {
      revenue: "42,642.00 ₽",
      model_cost: "8,989.82 ₽",
      search_cost: "1,839.60 ₽",
    },
    "e": {
      revenue: "42,642.00 ₽",
      model_cost: "8,989.82 ₽",
      search_cost: "1,839.60 ₽",
    },
    "f": {
      revenue: "42,642.00 ₽",
      model_cost: "8,989.82 ₽",
      search_cost: "1,839.60 ₽",
    },
    total_revenue: "253,409.00 ₽",
    total_model_cost: "19,986.50 ₽",
    total_search_cost: "19,986.50 ₽",
    model_cost_ratio: "7.89%",
    search_cost_ratio: "19.42%",
  },
])

const selectOpt = ref([])
const storeIds = ref([])

function onTimeChange(date, dateString) {
  console.log(date, dateString);
  getDataList(dateString[0], dateString[1]);
}

onMounted(() => {
  getDataList();
});


const handleChange = () => {
  getDataList();
};

const getDataList = (start_time = '', end_time = '') => {
  listApi({
    storeIds: storeIds.value,
    start_time,
    end_time,
  })
      .then((res) => {
        console.log(res);
        data.value = res.data;
      })
      .catch((err) => {
        console.log(err);
      });
}

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

.table-container {
  overflow-x: auto;
}

</style>

