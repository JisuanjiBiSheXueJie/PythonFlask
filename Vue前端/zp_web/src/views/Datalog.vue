<template>
    <div class="app_data">
        <div class="title">
            <h2>数据爬取日志</h2>
            <span>应用Python爬虫、Flask框架、Echarts、VUE等技术实现.</span>
        </div>
        <div class="update">
            <Table border :columns="columns1" :data="data1">
                <template #caozuo="{ row, index }">
                    <Button type="primary" size="small" @click="goDetail(row)"
                    >详情
                    </Button
                    >
                </template>
            </Table>
            <div class="page">
                <Page :total=pageInfo.total @on-change="ChangePage" show-total/>
            </div>
        </div>
        <Modal class="basicDataModal" :mask-closable="false" v-model="detailFlag" title="日志详细信息" footer-hide width="50">
            <div class="logDetail">
                <div ref="logContainer" class="log-container">
                    <pre>{{ detail.detail }}</pre>
                </div>
                <div class="dataSyncBtn" style="text-align: center;">
                    <Button style="width:90px;margin-right:15px" @click="canal">取消</Button>
                </div>
            </div>
        </Modal>
    </div>
</template>
<script>
import {getLog} from "@/api";

export default {
    data() {
        return {
            pageInfo: {
                pageNo: 1,
                pageSize: 10,
                total: 0,
                userRole: localStorage.getItem('role'),
                userName: localStorage.getItem('userName')
            },
            columns1: [
                {
                    title: '爬取关键词',
                    key: 'data_mode',
                    width: 120
                },
                {
                    title: '爬取数据条数',
                    key: 'data_num',
                    width: 140
                },
                {
                    title: '开始时间',
                    key: 'end_time',
                    width: 200
                },
                {
                    title: '结束时间',
                    key: 'end_time',
                    width: 200
                },
                {
                    title: '操作人',
                    key: 'user_name',
                    width: 100
                },
                {
                    title: '目标地址',
                    key: 'data_url',
                },
                {
                    title: '状态',
                    key: 'state',
                    width: 80,
                    render: (h, params) => {
                        let state = params.row.state;
                        if (state == '0') {
                            return h(
                                "span",
                                {
                                    style: {
                                        color: "red",
                                    },
                                },
                                "失败"
                            );
                        } else {
                            return h("span", {
                                style: {
                                    color: "#19be6b",
                                },
                            }, "成功");
                        }
                    },
                },
                {
                    title: "操作",
                    slot: "caozuo",
                    align: "center",
                    width: 80,
                },

            ],
            data1: [],
            detailFlag: false,
            detail: {}
        }
    },
    mounted() {
        this.init()
    },
    methods: {
        canal() {
            this.detailFlag = false;
        },
        goDetail(row, index) {
            this.detailFlag = true;
            this.detail = row;
        },
        async init() {
            const res = await getLog(this.pageInfo);
            this.pageInfo.total = res.total
            this.pageInfo.pageNo = res.pageno
            this.pageInfo.pageSize = res.pagesize
            this.data1 = res.info
        },
        ChangePage(e) {
            this.pageInfo.pageNo = e
            this.init()
        },
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

.page {
    text-align: center;
    padding: 10px;
}
</style>
