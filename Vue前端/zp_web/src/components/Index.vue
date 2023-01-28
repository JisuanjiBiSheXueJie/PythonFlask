<template>
    <div class="index-vue">
        <!-- 右侧部分 -->
        <section class="sec-right">
            <!-- 头部 -->
            <div class="top-c">
                <header style="border-radius: 8px;padding: 0 50px 0 50px;">
                    <div class="h-left" @click="gotoPage('data','')">
                        <div class="logo-c">
                            <!-- <img src="../assets/imgs/logo.png" alt="logo" class="logo">-->
                            <span>招聘信息可视化系统</span>
                        </div>
                    </div>
                    <div class="h-right">
                        <!-- 动态菜单 -->
                        <div class="h-menu" v-for="(item, index) in menuItems" :key="index"  @click="gotoPage(item.name,'')">
                            <Icon v-if="!item.hidden" :size="item.size" :type="item.type"/>
                            <span v-if="!item.hidden">{{item.text}}</span>
                        </div>
                        <!-- 用户头像 -->
                        <div class="user-img-c">
                            <img :src="userImg">
                        </div>
                        <!-- 下拉菜单 -->
                        <Dropdown trigger="click" @on-click="userOperate" @on-visible-change="showArrow">
                            <div class="pointer">
                                <span>{{userName}}</span>
                                <Icon v-show="arrowDown" type="md-arrow-dropdown"/>
                                <Icon v-show="arrowUp" type="md-arrow-dropup"/>
                            </div>
                            <DropdownMenu slot="list">
                                <!-- name标识符 -->
                                <DropdownItem name="1">修改密码</DropdownItem>
                                <DropdownItem name="2" v-if="userRole == '1'">获取数据</DropdownItem>
                                <DropdownItem name="4" v-if="userRole == '1'">爬取日志</DropdownItem>
                                <DropdownItem name="5" v-if="userRole == '1'">用户管理</DropdownItem>
                                <DropdownItem divided  name="3">退出登陆</DropdownItem>
                            </DropdownMenu>
                        </Dropdown>
                    </div>
                </header>
            </div>
            <!-- 页面主体 -->
            <div class="main-content">
                <div class="view-c">
                    <keep-alive :include="keepAliveData">
                        <!-- 子页面 -->
                        <router-view v-if="isShowRouter"/>
                    </keep-alive>
                </div>
            </div>
            <div class="m-footer">
                <span>Copyright © 2021.Company name All rights reserved.</span>
            </div>
        </section>
    </div>
</template>

<script>
import { resetTokenAndClearUser } from '../utils'

export default {
    name: 'index',
    data() {
        return {
            // 用于储存页面路径
            paths: {},
            // 当前显示页面
            currentPage: '',
            openMenus: [], // 要打开的菜单名字 name属性
            menuCache: [], // 缓存已经打开的菜单
            hasNewMsg: true, // 是否有新消息
            isShowRouter: true,
            msgNum: '10', // 新消息条数
            // 标签栏         标签标题     路由名称
            // 数据格式 {text: '首页', name: 'home'}
            // 用于缓存打开的路由 在标签栏上展示
            tagsArry: [],
            arrowUp: false, // 用户详情向上箭头
            arrowDown: true, // 用户详情向下箭头
            main: null, // 页面主要内容区域
            asideClassName: 'aside-big', // 控制侧边栏宽度变化
            asideArrowIcons: [], // 缓存侧边栏箭头图标 收缩时用
            // 面包屑
            crumbs: '主页',
            userName: '',
            userImg: '',
            userRole:'',
            // 主页路由名称
            home: 'data',
        }
    },
    mounted() {
        // 第一个标签
        const name = this.$route.name
        this.currentPage = name
        this.tagsArry.push({
            text: this.nameToTitle[name],
            name,
        })
        // 设置用户信息
        if (localStorage.getItem('userName')) {
            this.userName = localStorage.getItem('userName')
            this.userImg = localStorage.getItem('userImg')
            this.userRole = localStorage.getItem('role')
        }
        this.main = document.querySelector('.sec-right')
        this.asideArrowIcons = document.querySelectorAll('aside .ivu-icon-ios-arrow-down')
    },
    computed: {
        // 菜单栏
        menuItems() {
            return this.$store.state.menuItems
        },
        // 需要缓存的路由
        keepAliveData() {
            return this.tagsArry.map(item => item.name)
        },
        // 由于iView的导航菜单比较坑 只能设定一个name参数
        // 所以需要在这定义组件名称和标签栏标题的映射表 有多少个页面就有多少个映射条数
        nameToTitle() {
            const obj = {}
            this.menuItems.forEach(e => {
                this.processNameToTitle(obj, e)
            })

            return obj
        },
    },
    methods: {
        // 跳转页面 路由名称和参数
        gotoPage(name, params) {
            this.currentPage = name
            this.crumbs = this.paths[name]
            this.$router.push({ name, params })

            if (!this.keepAliveData.includes(name)) {
                // 如果标签超过8个 则将第一个标签删除
                if (this.tagsArry.length == 8) {
                    this.tagsArry.shift()
                }
                this.tagsArry.push({ name, text: this.nameToTitle[name] })
            }
        },
        // 用户操作
        userOperate(name) {
            switch (name) {
                case '1':
                    // 修改密码
                    this.gotoPage('password')
                    this.$router.push('password')
                    break
                case '2':
                    // 获取数据
                    this.gotoPage('getdata')
                    break
                case '3':
                    resetTokenAndClearUser()
                    this.$router.push({ name: 'data' })
                    break
                case '4':
                    this.gotoPage('datalog')
                    break
                case '5':
                    this.gotoPage('userlist')
                    break
            }
        },
        // 控制用户三角箭头显示状态
        showArrow(flag) {
            this.arrowUp = flag
            this.arrowDown = !flag
        },
        processNameToTitle(obj, data, text) {
            if (data.name) {
                obj[data.name] = data.text
                this.paths[data.name] = text ? `${text} / ${data.text}` : data.text
            }
            if (data.children) {
                data.children.forEach(e => {
                    this.processNameToTitle(obj, e, text ? `${text} / ${data.text}` : data.text)
                })
            }
        },
    },
}
</script>

<style scoped>
.index-vue {
    height: 100%;
    color: #666;
}
.top-c{
    padding: 0;
}
.logo-c {
    display: flex;
    align-items: center;
    color: rgba(255,255,255,.8);
    font-size: 16px;
    margin: 20px 0;
    justify-content: center;
}
.logo {
    width: 40px;
    margin-right: 10px;
}
.aside-big {
    width: 220px;
}
/* 主体页面 */
.sec-right {
    height: 100%;
    transition: margin-left .3s;
    overflow: hidden;;
    background: #f3f7fd;
}
/* 主体页面头部 */
header {
    height: 100px;
    border-bottom: none;
    background: #fff;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-right: 40px;
    padding-left: 10px;
    font-size: 14px;
}
header .ivu-icon {
    font-size: 24px;
    margin-right: 5px;
}
.h-right {
    display: flex;
    align-items: center;
}
.h-left {
    display: flex;
    align-items: center;
    cursor: pointer;
}
.user-img-c img {
    width: 100%;
}
.user-img-c {
    width: 34px;
    height: 34px;
    line-height: 34px;
    background: #ddd;
    border-radius: 50%;
    margin: 0 15px;
    overflow: hidden;
}
.ul-c li {
    border-radius: 3px;
    cursor: pointer;
    font-size: 12px;
    height: 24px;
    padding: 0 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 3px 5px 2px 3px;
    border: 1px solid #e6e6e6;
}
a {
    color: #666;
    transition: none;
}
.ul-c .ivu-icon {
    margin-left: 6px;
}
.active a {
    color: #fff;
}
.active .ivu-icon {
    color: #fff;
}
/* 主要内容区域 */
.main-content {
    height: calc(89% - 88px);
    overflow: hidden;
}
.view-c {
    position: relative;
    height: 100%;
    overflow: hidden;
}
.pointer {
    cursor: pointer;
}
.menu-level-3 .ivu-icon {
    font-size: 18px;
}
.external > i {
    margin-right: 6px;
}
.h-menu{
    height: 34px;
    line-height: 34px;
    margin: 0 20px;
    cursor:pointer;
}
.logo-c span{
    color: #1c5c93;
    font-size: 28px;
    margin: 0;
    padding: 10px 0;
    line-height: 1;
    font-weight: 400;
    letter-spacing: 3px;
    text-transform: uppercase;
}
.m-footer {
    display: flex;
    background: #587187;
    color: #fff;
    font-size: 14px;
    font-weight: 400;
    line-height: 1.5;
    height: 90px;
    line-height: 90px;
}
.m-footer span {
    width: 100%;
    text-align: center;
}
</style>
