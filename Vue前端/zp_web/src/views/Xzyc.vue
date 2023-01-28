<template>
    <div class="app_data">
        <div class="title">
            <h2>薪资预测</h2>
            <span>应用Python爬虫、Flask框架、Echarts、VUE等技术实现.</span>
        </div>
        <div class="update">
                <Form ref="formInline" :model="formLeft" :rules="formLeft" inline style="text-align: center;padding-top: 20px;">
                    <div>
                        <FormItem prop="search">
                            <Input v-model="formLeft.search" placeholder="行业"></Input>
                        </FormItem>
                        <FormItem prop="location">
                            <Input v-model="formLeft.location" placeholder="工作地点"></Input>
                        </FormItem>
                        <FormItem prop="xueli">
                            <FormItem>
                                <Select v-model="formLeft.xueli" style="width:200px" placeholder="请选择学历" clearable>
                                    <Option v-for="item in xueliList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                                </Select>
                            </FormItem>
                        </FormItem>
                    </div>

                    <div>
                        <FormItem prop="user">
                            <Select v-model="formLeft.jingyan" style="width:200px" placeholder="请选择工作经验" clearable>
                                <Option v-for="item in jingyanList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                            </Select>
                        </FormItem>
                        <FormItem prop="user">
                            <Select v-model="formLeft.company" style="width:200px" placeholder="请选择公司规模" clearable>
                                <Option v-for="item in companySize" :value="item.value" :key="item.value">{{ item.label }}</Option>
                            </Select>
                        </FormItem>
                        <FormItem prop="user">
                            <Select v-model="formLeft.companytype_text" style="width:200px" placeholder="请选择公司性质" clearable>
                                <Option v-for="item in companyXz" :value="item.value" :key="item.value">{{ item.label }}</Option>
                            </Select>
                        </FormItem>
                    </div>
                    <div>
                        <FormItem>
                            <Button type="success" @click="handleSubmit('formInline')">开始预测</Button>
                        </FormItem>
                    </div>

                </Form>
                <div class="xinzi">
                    <div class="xinzi_d">
                        <span class="xinzi_x" v-if="xinzi > 0" >预测结果：￥</span>
                        <span class="xinzi_x" v-if="xinzi > 0" >{{ xinzi }}</span>
                        <p v-if="xinzi > 0" >（结果仅供参考）</p>
                        <span v-if="xinzi == 0" >暂无结果，请爬取更多数据或更换查询条件重试</span>
                    </div>
                </div>
        </div>

    </div>
</template>
<script>
import {yuce,getXueli,jingyan,getComSize,getComXz} from "@/api";
export default {
    data() {
        return {
            formLeft: {
                search:'',
                location: '',
                xueli: '',
                jingyan:'',
                company:'',
                companytype_text:''
            },
            log:'',
            xinzi:-1,
            xueliList: [],
            jingyanList:[],
            companySize:[],
            companyXz:[]
        }
    },
    mounted() {
        this.getXueliList()
        this.getJIngyan()
        this.getComSize()
        this.getComXz()
    },
    methods:{
        async getComSize() {
            const res = await getComSize();
            this.companySize = res.info;
        },
        async getComXz() {
            const res = await getComXz();
            this.companyXz = res.info;
        },
        async getJIngyan() {
            const res = await jingyan();
            this.jingyanList = res.info;
        },
        async getXueliList() {
            const res = await getXueli();
            this.xueliList = res.info;
        },
        async handleSubmit() {
            if(!this.formLeft.search){
                this.$Message.warning("请输入行业");
                return
            }
            const res = await yuce(this.formLeft)
            this.xinzi = res.info
        }
    }
}
</script>
<style>
.app_data {
    width: 100%;
    height: 100%;
    background: #ffffff;
    padding: 0 10px;
    font-family: "Open Sans", sans-serif;
    color: #444;
}

.title {
    margin: 4px auto;
    padding: 30px;
    text-align: center;
}

.title h2{
    font-size: 32px;
    font-weight: 600;
    margin-bottom: 20px;
    padding-bottom: 0;
    color: #5c768d;
}

.title span{
    font-size: 16px;
    color: #444;
    font-family: "Open Sans", sans-serif;
}

.update {
    background: #f5f9fc;
}
.xinzi{
    padding: 10px 50px 50px 50px;
    text-align: center;
    height: 375px;
}
.xinzi_d{
    background: #e8e9f3;
    height: 100%;
    padding: 100px 0 0 0;
    width: 50%;
    margin-left: 25%;
    text-align: center;
}
.xinzi_x{
    font-family: emoji;
    font-size: 32px;
    color: #f55512;
    font-weight: 600;
}
</style>
