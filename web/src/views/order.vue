<template>
  <div>
    <!--页面区域-->
    <div class="page-view">
      <div class="table-operations">
        <a-space>
          <a-range-picker>
            <template slot="dateRender" slot-scope="current">
              <div class="ant-calendar-date" :style="getCurrentStyle(current)">
                {{ current.date() }}
              </div>
            </template>
          </a-range-picker>
          <a-button type="primary" @click="handleAdd">新增</a-button>
          <a-button @click="handleBatchDelete">批量删除</a-button>
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
          :row-selection="rowSelection"
          :pagination="{
          size: 'default',
          current: data.page,
          pageSize: data.pageSize,
          onChange: (current) => (data.page = current),
          showSizeChanger: false,
          showTotal: (total) => `共${total}条数据`,
        }"
      >
        <template #bodyCell="{ text, record, index, column }">
          <template v-if="column.key === 'operation'">
            <span>
              <a @click="handleEdit(record)">编辑</a>
              <a-divider type="vertical"/>
              <a-popconfirm title="确定删除?" ok-text="是" cancel-text="否" @confirm="confirmDelete(record)">
                <a href="#">删除</a>
              </a-popconfirm>
            </span>
          </template>
        </template>
      </a-table>
    </div>

    <!--弹窗区域-->
    <div>
      <a-modal
          :visible="modal.visile"
          :forceRender="true"
          :title="modal.title"
          width="880px"
          ok-text="确认"
          cancel-text="取消"
          @cancel="handleCancel"
          @ok="handleOk"
      >
        <template #footer>
          <a-button key="back" @click="handleCancel">取消</a-button>
          <a-button key="submit" type="primary" :loading="submitting" @click="handleOk">确认</a-button>
        </template>
        <div style="padding-right: 16px; max-height:480px; overflow-x: hidden;overflow-y: auto;">
          <a-form ref="myform" :label-col="{ style: { width: '80px' } }" :model="modal.form" :rules="modal.rules">
            <a-row :gutter="24">
              <a-col span="12">
                <a-form-item label="店铺" name="store_name">
                  <a-input placeholder="请输入" v-model:value="modal.form.store_name"></a-input>
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="订单编号" name="order_number">
                  <a-input placeholder="请输入" v-model:value="modal.form.order_number"></a-input>
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="订单总金额" name="order_amount">
                  <a-input placeholder="请输入" v-model:value="modal.form.order_amount"></a-input>
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="下单时间" name="order_amount">
                  <a-input placeholder="请输入" v-model:value="modal.form.order_amount"></a-input>
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="运输时间" name="shipment_time">
                  <a-input placeholder="请输入" v-model:value="modal.form.shipment_time"></a-input>
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="订购数量" name="count">
                  <a-input placeholder="请输入" v-model:value="modal.form.count"></a-input>
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="SKU" name="sku">
                  <a-input placeholder="请输入" v-model:value="modal.form.sku"></a-input>
                </a-form-item>
              </a-col>
              <a-col span="12">
                <a-form-item label="状态" name="status">
                  <a-select placeholder="请选择" allowClear v-model:value="modal.form.status">
                    <a-select-option key="0" value="0">运输中</a-select-option>
                    <a-select-option key="1" value="1">已签收</a-select-option>
                    <a-select-option key="2" value="2">退货中</a-select-option>
                    <a-select-option key="99" value="99">退货重新上架</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
            </a-row>
          </a-form>
        </div>
      </a-modal>
    </div>
  </div>
</template>

<script setup lang="ts">
import {FormInstance, message, SelectProps} from 'ant-design-vue';
import {createApi, listApi, updateApi, deleteApi} from '/@/api/order';
import {listApi as listClassificationApi} from '/@/api/classification'
import {listApi as listTagApi} from '/@/api/tag'
import {BASE_URL} from "/@/store/constants";
import {FileImageOutlined, VideoCameraOutlined} from '@ant-design/icons-vue';

const columns = reactive([

  {
    title: '序号',
    dataIndex: 'id',
    key: 'id',
    width: 60
  },
  {
    title: '店铺',
    dataIndex: 'store_name',
    key: 'store_name'
  },
  {
    title: '订单编号',
    dataIndex: 'order_number',
    key: 'order_number'
  },
  {
    title: 'SKU',
    dataIndex: 'sku',
    key: 'sku'
  },
  {
    title: '订单总金额',
    dataIndex: 'order_amount',
    key: 'order_amount'
  },
  {
    title: '下单时间',
    dataIndex: 'order_time',
    key: 'order_time'
  },
  {
    title: '运输时间',
    dataIndex: 'shipment_time',
    key: 'shipment_time'
  },
  {
    title: '订购数量',
    dataIndex: 'count',
    key: 'count'
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    customRender: ({text, record, index, column}) => {
      switch (text) {
        case '0':
          return '运输中';
        case '1':
          return '已签收';
        case '2':
          return '退货中';
        case '99':
          return '退货重新上架';
        default:
          return '';
      }
    }
  },
  {
    title: '操作',
    dataIndex: 'action',
    key: 'operation',
    align: 'center',
    fixed: 'right',
    width: 140,
  },
]);


// 文件列表
const fileList = ref<any[]>([]);

const submitting = ref<boolean>(false);

// 页面数据
const data = reactive({
  dataList: [],
  loading: false,
  keyword: '',
  selectedRowKeys: [] as any[],
  pageSize: 10,
  page: 1,
});

// 弹窗数据源
const modal = reactive({
  visile: false,
  editFlag: false,
  title: '',
  cData: [],
  tagData: [{}],
  form: {
    id: undefined,
    order_number: undefined,
    sku: undefined,
    status: undefined,
    order_amount: undefined,
    order_time: undefined,
    count: undefined,
    store_name: undefined,
    shipment_time: undefined
  },
  rules: {
    order_number: [{required: true, message: '请输入', trigger: 'change'}],
    sku: [{required: true, message: '请输入', trigger: 'change'}],
    status: [{required: true, message: '请输入', trigger: 'change'}],
    order_amount: [{required: true, message: '请输入', trigger: 'change'}],
    order_time: [{required: true, message: '请输入', trigger: 'change'}],
    count: [{required: true, message: '请输入', trigger: 'change'}],
    store_name: [{required: true, message: '请输入', trigger: 'change'}],
    shipment_time: [{required: true, message: '请选择状态', trigger: 'change'}]
  },
});

const myform = ref<FormInstance>();

onMounted(() => {
  getDataList();
  getCDataList();
  getTagDataList();
});

const getDataList = () => {
  data.loading = true;
  listApi({
    keyword: data.keyword,
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

const getCDataList = () => {
  listClassificationApi({}).then(res => {
    modal.cData = res.data
  })
}
const getTagDataList = () => {
  listTagApi({}).then(res => {
    res.data.forEach((item, index) => {
      item.index = index + 1
    })
    modal.tagData = res.data
  })
}

const onSearchChange = (e: Event) => {
  data.keyword = e?.target?.value;
  console.log(data.keyword);
};

const onSearch = () => {
  getDataList();
};

const rowSelection = ref({
  onChange: (selectedRowKeys: (string | number)[], selectedRows: DataItem[]) => {
    console.log(`selectedRowKeys: ${selectedRowKeys}`, 'selectedRows: ', selectedRows);
    data.selectedRowKeys = selectedRowKeys;
  },
});

const handleAdd = () => {
  resetModal();
  modal.visile = true;
  modal.editFlag = false;
  modal.title = '新增';
  // 重置
  for (const key in modal.form) {
    modal.form[key] = undefined;
  }
  modal.form.cover = undefined
};
const handleEdit = (record: any) => {
  resetModal();
  modal.visile = true;
  modal.editFlag = true;
  modal.title = '编辑';
  // 重置
  for (const key in modal.form) {
    modal.form[key] = undefined;
  }
  for (const key in record) {
    if (record[key]) {
      modal.form[key] = record[key];
    }
  }
  if (modal.form.cover) {
    modal.form.coverUrl = BASE_URL + modal.form.cover
    modal.form.cover = undefined
  }
};

const confirmDelete = (record: any) => {
  console.log('delete', record);
  deleteApi({ids: record.id})
      .then((res) => {
        getDataList();
      })
      .catch((err) => {
        message.error(err.msg || '操作失败');
      });
};

const handleBatchDelete = () => {
  console.log(data.selectedRowKeys);
  if (data.selectedRowKeys.length <= 0) {
    console.log('hello');
    message.warn('请勾选删除项');
    return;
  }
  deleteApi({ids: data.selectedRowKeys.join(',')})
      .then((res) => {
        message.success('删除成功');
        data.selectedRowKeys = [];
        getDataList();
      })
      .catch((err) => {
        message.error(err.msg || '操作失败');
      });
};

const handleOk = () => {
  myform.value
      ?.validate()
      .then(() => {
        const formData = new FormData();
        if (modal.editFlag) {
          formData.append('id', modal.form.id)
        }
        formData.append('order_number', modal.form.order_number || '')
        formData.append('sku', modal.form.sku || '')
        formData.append('status', modal.form.status || '')
        formData.append('order_amount', modal.form.order_amount || '')
        formData.append('order_time', modal.form.order_time || '')
        formData.append('shipment_time', modal.form.shipment_time || '')
        formData.append('count', modal.form.count || '')
        formData.append('store_name', modal.form.store_name || '')


        if (modal.editFlag) {
          submitting.value = true
          updateApi({
            id: modal.form.id
          }, formData)
              .then((res) => {
                submitting.value = false
                hideModal();
                getDataList();
              })
              .catch((err) => {
                submitting.value = false
                console.log(err);
                message.error(err.msg || '操作失败');
              });
        } else {
          submitting.value = true
          createApi(formData)
              .then((res) => {
                submitting.value = false
                hideModal();
                getDataList();
              })
              .catch((err) => {
                submitting.value = false
                console.log(err);
                message.error(err.msg || '操作失败');
              });
        }
      })
      .catch((err) => {
        console.log('不能为空');
      });
};

const handleCancel = () => {
  hideModal();
};

// 恢复表单初始状态
const resetModal = () => {
  myform.value?.resetFields();
  fileList.value = []
};

// 关闭弹窗
const hideModal = () => {
  modal.visile = false;
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
