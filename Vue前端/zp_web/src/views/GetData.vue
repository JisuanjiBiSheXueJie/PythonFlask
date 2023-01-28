<template>
    <div class="app_data">
        <div class="title">
            <h2>动态爬取数据</h2>
            <span>应用Python爬虫、Flask框架、Echarts、VUE等技术实现.</span>
        </div>
        <div class="update">
                <Form ref="formInline" :model="formLeft" :rules="formLeft" inline style="text-align: center;padding-top: 20px;">
                    <FormItem prop="user">
                        <Input v-model="formLeft.search" placeholder="请输入爬取关键词"></Input>
                    </FormItem>
                    <FormItem prop="password">
                        <Select v-model="formLeft.city_id" style="width:200px" placeholder="请选择城市" default-label="2页">
                            <Option v-for="item in cityList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                        </Select>
                    </FormItem>
                    <FormItem prop="password">
                        <Select v-model="formLeft.pageSize" style="width:200px" placeholder="请选择爬取页数" default-label="2页">
                            <Option v-for="item in pageList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                        </Select>
                    </FormItem>
                    <FormItem>
                        <Button type="primary" @click="handleSubmit('formInline')">开始爬取</Button>
                    </FormItem>
                </Form>
            <span style="padding: 0 0 10px 10px;">日志：</span>
            <Input  :rows="20" style="margin: 0 10px 10px 10px;width: 99%" v-model="log" type="textarea" readonly/>
        </div>

    </div>
</template>
<script>
import {getJobData,getCityDict} from "@/api";
export default {
    data() {
        return {
            formLeft: {
                username:localStorage.getItem('userName')||'',
                search: '',
                pageSize: '',
                city_id:''
            },
            log:'',
            pageList: [
                {
                    value: 2,
                    label: '2页'
                },
                {
                    value: 5,
                    label: '5页'
                },
                {
                    value: 10,
                    label: '10页'
                },
                {
                    value: 15,
                    label: '15页'
                }
            ],
            cityList:[]
        }
    },
    mounted() {
        this.getCiytList()
    },
    methods:{
        async getCiytList() {
            const res = await getCityDict()
            if (res.code == 200) {
                this.cityList = res.info
            }
        },
        async handleSubmit() {
            if(!this.formLeft.pageSize){
                this.$Message.warning('请选择爬取页数!');
                return
            }
            const res = await getJobData(this.formLeft)
            this.log = res.info ;
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
</style>
