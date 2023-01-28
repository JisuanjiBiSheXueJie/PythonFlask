import request from '@/utils/request'

export function fetchUserData() {
    return request.get('https://api.github.com/users/woai3c')
}

// 登录
export function login(params) {
    return request.post('/api/login' , params)
}

// 注册
export function reg(params) {
    return request.post('/api/reg' , params)
}

// 修改密码
export function changePwd(params) {
    return request.post('/api/changePwd' , params)
}

// 爬取数据
export function getJobData(params) {
    return request.post('/api/getJobData' , params)
}

// 获取日志
export function getLog(params) {
    return request.post('/api/getLogs' , params)
}

// 数据概览
export function getdatas(params) {
    return request.post('/api/getDatas' , params)
}

// 城市招聘分布
export function getZpcity(params) {
    return request.post('/api/zpcity' , params)
}

// 城市薪资统计
export function getZpXinzi(params) {
    return request.post('/api/zpXinzi' , params)
}

// 学历要求
export function getXueli(params) {
    return request.post('/api/xueli' , params)
}

// 经验要求
export function jingyan(params) {
    return request.post('/api/jingyan' , params)
}

// 招聘要求
export function yaoqiu(params) {
    return request.post('/api/yaoqiu' , params)
}

// 生成福利词云
export function getCiyun(params) {
    return request.post('/api/fuli' , params)
}

// 公司信息统计
export function gsinfo(params) {
    return request.post('/api/gsinfo' , params)
}

// 薪资预测
export function yuce(params) {
    return request.post('/api/yuce' , params)
}

// 用户列表
export function getUsers(params) {
    return request.post('/api/getUsers' , params)
}

// 用户删除
export function delUser(params) {
    return request.post('/api/delUser' , params)
}

// 用户启用
export function startUser(params) {
    return request.post('/api/startUser' , params)
}

// 用户停用
export function stopUser(params) {
    return request.post('/api/stopUser' , params)
}

// 用户编辑
export function editUser(params) {
    return request.post('/api/editUser' , params)
}

// 用户新增
export function addUser(params) {
    return request.post('/api/addUser' , params)
}

// 重置密码
export function chongzhi(params) {
    return request.post('/api/chongzhi' , params)
}

// 删除数据
export function delData(params) {
    return request.post('/api/delData' , params)
}

// 城市字典表
export function getCityDict(params) {
    return request.post('/api/getCityDict' , params)
}

// 公司性质
export function getComXz(params) {
    return request.post('/api/getComXz' , params)
}

// 公司规模
export function getComSize(params) {
    return request.post('/api/getComSize' , params)
}

// 收藏
export function collect(params) {
    return request.post('/api/collect' , params)
}

// 取消收藏
export function delCollect(params) {
    return request.post('/api/delCollect' , params)
}