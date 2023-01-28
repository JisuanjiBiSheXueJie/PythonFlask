<template>
    <div class="reg-vue" :style="bg">
        <div class="container">
            <p class="title">欢迎注册</p>
            <div class="input-c">
                <div class="wenzi">
                    <span>登录账号</span>
                </div>
                <Input  v-model="account" placeholder="登录账号" clearable @on-blur="verifyAccount"/>
                <p class="error">{{ accountError }}</p>
            </div>
            <div class="input-c">
                <div class="wenzi">
                    <span>用户姓名</span>
                </div>
                <Input type="text" v-model="name"  placeholder="用户姓名" clearable @on-blur="verifyName"
                       @keyup.enter.native="submit"/>
                <p class="error">{{ nameERror }}</p>
            </div>
            <div class="input-c">
                <div class="wenzi">
                    <span>密&nbsp;&nbsp;&nbsp;&nbsp;码</span>
                </div>
                <Input type="password" v-model="pwd"  placeholder="密码" clearable @on-blur="verifyPwd"
                       @keyup.enter.native="submit"/>
                <p class="error">{{ pwdError }}</p>
            </div>
            <div class="input-c">
                <div class="wenzi">
                    <span>确认密码</span>
                </div>
                <Input type="password" v-model="pwd2"  placeholder="密码" clearable @on-blur="verifyPwd2"
                       @keyup.enter.native="submit"/>
                <p class="error">{{ pwd2Error }}</p>
            </div>
            <Button :loading="isShowLoading" class="submit" type="primary" @click="submit">注册</Button>
            <p class="account"><span @click="register">已有账号，去登录</span></p>
        </div>
    </div>
</template>

<script>
import {reg} from "../api";

export default {
    name: 'reg',
    data() {
        return {
            account: '',
            name:'',
            pwd: '',
            pwd2:'',
            accountError: '',
            nameERror:'',
            pwdError: '',
            pwd2Error:'',
            isShowLoading: false,
            bg: {},
        }
    },
    created() {
        this.bg.backgroundImage = 'url(' + require('../assets/imgs/bg06.jpg') + ')'
    },
    watch: {
        $route: {
            handler(route) {
                this.redirect = route.query && route.query.redirect
            },
            immediate: true,
        },
    },
    methods: {
        verifyAccount() {
            if (!this.account) {
                this.accountError = '请输入登录账号'
            } else {
                this.accountError = ''
            }
        },
        verifyName() {
            if (!this.name) {
                this.nameERror = '请输入用户姓名'
            } else {
                this.nameERror = ''
            }
        },
        verifyPwd() {
            if (!this.pwd) {
                this.pwdError = '请输入密码'
            } else {
                this.pwdError = ''
            }
        },
        verifyPwd2() {
            if (!this.pwd2) {
                this.pwd2Error = '请输入确认密码'
            } else if(this.pwd != this.pwd2){
                this.pwd2Error = '确认密码不正确'
            } else {
                this.pwd2Error = ''
            }
        },
        register() {
            this.$router.push('login')
        },
        forgetPwd() {

        },
        async submit() {
            if (!this.account) {
                this.$Message.warning('请输入账号')
                return
            }
            if (!this.pwd) {
                this.$Message.warning('请输入密码') ;
                return
            }
            if (!this.pwd2) {
                this.$Message.warning('请输入确认密码') ;
                return
            }
            if (!this.name) {
                this.$Message.warning('请输入用户姓名') ;
                return
            }
            if (this.pwd != this.pwd2) {
                this.$Message.warning('确认密码输入不正确') ;
                return
            }
            const res = await reg(`account=${this.account}&pwd=${this.pwd}&name=${this.name}`)
            debugger
            if (res.code == 200){
                this.isShowLoading = true
                this.$Message.success(res.info);
                this.timer = setTimeout(()=>{
                    this.$router.push({path: this.redirect || '/'})
                },1000);
            } else {
                this.$Message.error(res.info);
                return
            }
        },
    },
}
</script>

<style>
.reg-vue {
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #fff;
}

.reg-vue .container {
    background: rgba(255, 255, 255, .5);
    width: 400px;
    text-align: center;
    border-radius: 10px;
    padding: 30px;
}

.reg-vue .ivu-input {
    background-color: transparent;
    color: #fff;
    outline: #fff;
    border-color: #fff;
}

.reg-vue ::-webkit-input-placeholder { /* WebKit, Blink, Edge */
    color: rgba(255, 255, 255, .8);
}

.reg-vue :-moz-placeholder { /* Mozilla Firefox 4 to 18 */
    color: rgba(255, 255, 255, .8);
}

.reg-vue ::-moz-placeholder { /* Mozilla Firefox 19+ */
    color: rgba(255, 255, 255, .8);
}

.reg-vue :-ms-input-placeholder { /* Internet Explorer 10-11 */
    color: rgba(255, 255, 255, .8);
}

.reg-vue .title {
    font-size: 16px;
    margin-bottom: 20px;
}

.reg-vue .input-c {
    margin: auto;
    width: 350px;
}

.reg-vue .error {
    color: red;
    text-align: left;
    margin: 5px auto;
    font-size: 12px;
    padding-left: 30px;
    height: 20px;
}

.reg-vue .submit {
    width: 308px;
    margin: 0 0 0 13px;
}

.reg-vue .account {
    margin: 25px 23px 0 0;
    float: right;
    border-bottom: 1px #fff solid;
    font-size: 10px;
}

.reg-vue .account span {
    cursor: pointer;
}

.reg-vue .ivu-icon {
    color: #eee;
}

.reg-vue .ivu-icon-ios-close-circle {
    color: #777;
}

</style>
<style scoped>
.ivu-input-wrapper{
    width: 70%;
    display: inline-block;
}
.wenzi{
    width: 20%;
    display: inline-block;
}
.wenzi span{
   margin: 0 14px 0 0;
}
</style>
