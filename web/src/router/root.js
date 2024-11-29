// 路由表
const constantRouterMap = [

    {
        path: '/', redirect: '/admin',
    }, {
        path: '/adminLogin', name: 'adminLogin', component: () => import('/@/views/admin-login.vue'),
    }, {
        path: '/admin',
        name: 'admin',
        redirect: '/admin/thing',
        component: () => import('/@/views/main.vue'),
        children: [{
            path: 'overview', name: 'overview', component: () => import('/@/views/overview.vue')
        }, {path: 'thing', name: 'thing', component: () => import('/@/views/thing.vue')}, {
            path: 'finance', name: 'finance', component: () => import('/@/views/finance.vue')
        }, {path: 'order', name: 'order', component: () => import('/@/views/order.vue')}, {
            path: 'comment', name: 'comment', component: () => import('/@/views/comment.vue')
        }, {path: 'refund', name: 'refund', component: () => import('/@/views/refund.vue')}, {
            path: 'comment', name: 'comment', component: () => import('/@/views/comment.vue')
        }, {path: 'user', name: 'user', component: () => import('/@/views/user.vue')}, {
            path: 'classification', name: 'classification', component: () => import('/@/views/classification.vue')
        }, {path: 'tag', name: 'tag', component: () => import('/@/views/tag.vue')}, {
            path: 'ad', name: 'ad', component: () => import('/@/views/ad.vue')
        }, {path: 'notice', name: 'notice', component: () => import('/@/views/notice.vue')}, {
            path: 'loginLog', name: 'loginLog', component: () => import('/@/views/login-log.vue')
        }, {path: 'opLog', name: 'opLog', component: () => import('/@/views/op-log.vue')}, {
            path: 'errorLog', name: 'errorLog', component: () => import('/@/views/error-log.vue')
        }, {path: 'sysInfo', name: 'sysInfo', component: () => import('/@/views/sys-info.vue')}, {
            path: 'ad_cost', name: 'ad_cost', component: () => import('/@/views/ad_cost.vue')
        }, {
            path: 'store_ad', name: 'store_ad', component: () => import('/@/views/store_ad.vue')
        }, {
            path: 'refund_rank', name: 'refund_rank', component: () => import('/@/views/refund_rank.vue')
        }, {
            path: 'unsalable_rank', name: 'unsalable_rank', component: () => import('/@/views/unsalable_rank.vue')
        }, {
            path: 'profit_statement', name: 'profit_statement', component: () => import('/@/views/profit_statement.vue')
        },]
    },];

export default constantRouterMap;
