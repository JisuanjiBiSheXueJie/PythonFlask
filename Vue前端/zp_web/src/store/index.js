import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
        isShowLoading: false, // 全局 loading
        // 左侧菜单栏数据
        menuItems: [
            {
                type: 'ios-browsers-outline',
                name: 'data',
                text: '数据概览',
            },
            {
                type: 'ios-list-box-outline',
                name: 'zpcity',
                text: '城市招聘分布',
            },
            {
                type: 'ios-cloud-outline',
                name: 'zpfuli',
                text: '福利词云',
            },
            {
                type: 'ios-stats-outline',
                name: 'zpxinzi',
                text: '薪资统计',
            },
            {
                type: 'ios-paper-outline',
                name: 'zpyaoqiu',
                text: '招聘要求',
            },
            {
                type: 'ios-information-circle-outline',
                name: 'gsinfo',
                text: '公司信息分析',
            },
            {
                type: 'ios-paper-plane-outline',
                name: 'yuce',
                text: '薪资预测',
            },
            {
                type: 'md-lock',
                name: 'password',
                text: '修改密码',
                hidden: true,
            },
            {
                type: 'md-person',
                name: 'getdata',
                text: '获取数据',
                hidden: true,
            },
            {
                type: 'md-person',
                name: 'datalog',
                text: '爬取日志', 
                hidden: true,
            },
            {
                type: 'md-person',
                name: 'userlist',
                text: '用户管理', 
                hidden: true,
            },
        ],
    },
    mutations: {
        setMenus(state, items) {
            state.menuItems = [...items]
        },
        setLoading(state, isShowLoading) {
            state.isShowLoading = isShowLoading
        },
    },
})

export default store
