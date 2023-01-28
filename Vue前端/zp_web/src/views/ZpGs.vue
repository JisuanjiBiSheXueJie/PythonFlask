<template>
    <div class="app_data">
        <div class="title">
            <h2>公司信息统计分析</h2>
            <span>应用Python爬虫、Flask框架、Echarts、VUE等技术实现.</span>
        </div>
        <div class="query-c">
            <Form inline>
                <FormItem>
                    <Select v-model="searchParams.type" style="width:200px" placeholder="请选择统计类型">
                        <Option v-for="item in typeList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                </FormItem>
                <FormItem>
                    <Input type="text" v-model="searchParams.search" placeholder="职业类型"> </Input>
                </FormItem>
                <FormItem>
                    <Select v-model="searchParams.xueli" style="width:200px" placeholder="请选择学历">
                        <Option v-for="item in xueliList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                </FormItem>
                <FormItem>
                    <Input type="text" v-model="searchParams.location" placeholder="工作地点"> </Input>
                </FormItem>
                <FormItem>
                    <Button type="primary" @click="handleSubmit()">搜索</Button>
                </FormItem>
            </Form>
        </div>
        <div class="update">
            <div id="main" style="width: 40%; height: 500px;display: inline-block;border-right: #fff 2px solid;"></div>
            <div id="main2" style="width: 60%; height: 500px;display: inline-block;"></div>
        </div>

    </div>
</template>
<script>
import {gsinfo, getXueli} from "../api";

export default {
    name: 'hello',
    data() {
        return {
            eData: [],
            searchParams: {
                search: '',
                type: '',
                location: '',
                xueli:''
            },
            xueliList: [
               
            ],
            typeList: [
                // {label:'公司属性',value:'sx'},
                {label:'公司性质',value:'xz'},
                {label:'公司规模',value:'size'},
            ],
            xData:[],
            yData:[],
            type:''

        }
    },
    mounted() {
        this.init()
        this.getXueliList()
    },
    methods: {
        async getXueliList() {
            const res = await getXueli();
            this.xueliList = res.info;
        },
        handleSubmit() {
            this.init();
            this.xData = []
            this.yData = []
        },
        async init() {
            if(this.searchParams.type == ''){
                this.searchParams.type = 'xz'
            }
            const res = await gsinfo(`search=${this.searchParams.search}&type=${this.searchParams.type}&location=${this.searchParams.location}&xueli=${this.searchParams.xueli}`);
            this.eData = res.info
            res.info.forEach(item => {
                this.xData.push(item.name)
                this.yData.push(item.value)
            })
            if (res.type == 'sx') {
                this.type = '公司属性'
            } else if (res.type == 'xz') {
                this.type = '公司性质'
            } else {
                this.type = '公司规模'
            }
            this.drawChart();
            this.drawChart2();
        },
        drawChart() {
            // 基于准备好的dom，初始化echarts实例
            var myChart = this.$echarts.init(document.getElementById('main'));


            // 指定图表的配置项和数据
            var option = {
                title: {
                    subtext: this.type + '饼状图',
                },
                color: [
                    '#006cff', '#60cda0', '#ed8884', '#ff9f7f', '#0096ff', '#9fe6b8', '#32c5e9', '#1d9dff',
                    '#006cff', '#60cda0', '#ed8884', '#ff9f7f', '#0096ff', '#9fe6b8', '#32c5e9', '#1d9dff',
                    '#006cff', '#60cda0', '#ed8884', '#ff9f7f', '#0096ff', '#9fe6b8', '#32c5e9', '#1d9dff',
                    '#006cff', '#60cda0', '#ed8884', '#ff9f7f', '#0096ff', '#9fe6b8', '#32c5e9', '#1d9dff',
                    '#006cff', '#60cda0', '#ed8884', '#ff9f7f', '#0096ff', '#9fe6b8', '#32c5e9', '#1d9dff',
                    '#006cff', '#60cda0', '#ed8884', '#ff9f7f', '#0096ff', '#9fe6b8', '#32c5e9', '#1d9dff'
                ],
                legend: {
                    top: 'bottom',
                    textStyle: {
                        fontSize: 10,
                        color: '#000',
                    }
                },
                tooltip: {
                    trigger: 'item',
                    formatter: '{a} <br/>{b} : {c} ({d}%)'
                },
                series: [
                    {
                        name: '公司数占比',
                        type: 'pie',
                        radius: ['20%', '50%'],
                        center: ['50%', '50%'],
                        roseType: 'radius',
                        itemStyle: {
                            borderRadius: 8
                        },
                        data: this.eData,
                    }
                ]
            };


            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
            // 跟着缩放
            window.addEventListener('resize', function () {
                // 让我们的图表调用 resize这个方法
                myChart.resize();
            });
        },
        drawChart2() {
            // 基于准备好的dom，初始化echarts实例
            var myChart = this.$echarts.init(document.getElementById('main2'));

            var myColor = [
                "#1089E7", "#F57474", "#56D0E3", "#F8B448", "#8B78F6",
                "#1089E7", "#F57474", "#56D0E3", "#F8B448", "#8B78F6",
                "#1089E7", "#F57474", "#56D0E3", "#F8B448", "#8B78F6",
                "#1089E7", "#F57474", "#56D0E3", "#F8B448", "#8B78F6",
                "#1089E7", "#F57474", "#56D0E3", "#F8B448", "#8B78F6",
                "#1089E7", "#F57474", "#56D0E3", "#F8B448", "#8B78F6",
                "#1089E7", "#F57474", "#56D0E3", "#F8B448", "#8B78F6",
            ];

            // 指定图表的配置项和数据
            var option = {
                title: {
                    subtext: this.type + '柱状图',
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    }
                },
                grid: {
                    top: "10%",
                    left: '3%',
                    right: '6%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    data: this.xData,
                    //主要是下面的代码-倾斜
                    axisLabel:{ 
                        rotate : 60 
                    }
                },
                yAxis: {
                    type: 'value'
                },
                series: [
                    {
                        name: '公司数',
                        type: 'bar',
                        // 柱子设为圆角
                        itemStyle: {
                            normal: {
                                barBorderRadius: 20,
                                // dataIndex 是当前柱子的索引号
                                color: function (params) {
                                    return myColor[params.dataIndex];
                                }
                            }
                        },
                        data: this.yData,
                    }
                ]
            };


            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
            // 跟着缩放
            window.addEventListener('resize', function () {
                // 让我们的图表调用 resize这个方法
                myChart.resize();
            });
        }
    }
}

</script>
<style>
.app_data {
    width: 100%;
    height: 100%;
    background: #ffffff;
    padding: 0 200px;
    font-family: "Open Sans", sans-serif;
    color: #444;
}

.title {
    margin: 4px auto;
    padding: 30px;
    text-align: center;
}

.title h2 {
    font-size: 32px;
    font-weight: 600;
    margin-bottom: 20px;
    padding-bottom: 0;
    color: #5c768d;
}

.title span {
    font-size: 16px;
    color: #444;
    font-family: "Open Sans", sans-serif;
}

.update {
    background: #f5f9fc;
}
</style>
