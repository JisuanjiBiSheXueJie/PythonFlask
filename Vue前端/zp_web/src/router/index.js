import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const commonRoutes = [
    {
        path: '/login',
        name: 'login',
        meta: { title: '登录' },
        component: () => import('../components/Login.vue'),
    },
     {
        path: '/reg',
        name: 'reg',
        meta: { title: '注册' },
        component: () => import('../components/Reg.vue'),
    },
    {
        path: '/404',
        name: '404',
        meta: { title: '404' },
        component: () => import('../components/404.vue'),
    },
    { path: '/', redirect: '/data' },
]

// 本地所有的页面 需要配合后台返回的数据生成页面
export const asyncRoutes = {
    data: {
        path: 'data',
        name: 'data',
        meta: { title: '数据概览' },
        component: () => import('../views/Data.vue'),
    },
    zpcity: {
        path: 'zpcity',
        name: 'zpcity',
        meta: { title: '城市招聘分布' },
        component: () => import('../views/Zpcity.vue'),
    },
    zpfuli: {
        path: 'zpfuli',
        name: 'zpfuli',
        meta: { title: '福利词云' },
        component: () => import('../views/ZpFuli.vue'),
    },
    zpxinzi: {
        path: 'zpxinzi',
        name: 'zpxinzi',
        meta: { title: '薪资统计' },
        component: () => import('../views/ZpXinzi.vue'),
    },
    zpyaoqiu: {
        path: 'zpyaoqiu',
        name: 'zpyaoqiu',
        meta: { title: '招聘要求' },
        component: () => import('../views/ZpYaoqiu.vue'),
    },
    gsinfo: {
        path: 'gsinfo',
        name: 'gsinfo',
        meta: { title: '公司信息分析' },
        component: () => import('../views/ZpGs.vue'),
    },
    yuce: {
        path: 'yuce',
        name: 'yuce',
        meta: { title: '薪资预测' },
        component: () => import('../views/Xzyc.vue'),
    },
    password: {
        path: 'password',
        name: 'password',
        meta: { title: '修改密码' },
        component: () => import('../views/Password.vue'),
    },
    getdata: {
        path: 'getdata',
        name: 'getdata',
        meta: { title: '获取数据' },
        component: () => import('../views/GetData.vue'),
    },
    userinfo: {
        path: 'userinfo',
        name: 'userinfo',
        meta: { title: '用户信息' },
        component: () => import('../views/UserInfo.vue'),
    },
    datalog: {
        path: 'datalog',
        name: 'datalog',
        meta: { title: '爬取日志' }, 
        component: () => import('../views/Datalog.vue'),
    },
    userlist: {
        path: 'userlist',
        name: 'userlist',
        meta: { title: '用户管理' }, 
        component: () => import('../views/Userlist.vue'),
    },
}

const createRouter = () => new Router({
    routes: commonRoutes,
})

const router = createRouter()

export function resetRouter() {
    const newRouter = createRouter()
    router.matcher = newRouter.matcher
}

export default router
