<template>
    <div class="login-vue" :style="bg">
        <div class="container">
            <p class="title">欢迎登录</p>
            <div class="input-c">
                <Input prefix="ios-contact" v-model="account" placeholder="用户名" clearable @on-blur="verifyAccount"/>
                <p class="error">{{ accountError }}</p>
            </div>
            <div class="input-c">
                <Input type="password" v-model="pwd" prefix="md-lock" placeholder="密码" clearable @on-blur="verifyPwd"
                       @keyup.enter.native="submit"/>
                <p class="error">{{ pwdError }}</p>
            </div>
            <Button :loading="isShowLoading" class="submit" type="primary" @click="submit">登陆</Button>
            <p class="account"><span @click="register('reg','')">没有账号，注册一个</span></p>
        </div>
    </div>
</template>

<script>
import {login} from "../api";

export default {
    name: 'login',
    data() {
        return {
            account: '',
            pwd: '',
            accountError: '',
            pwdError: '',
            isShowLoading: false,
            bg: {},
        }
    },
    created() {
        this.bg.backgroundImage = 'url(' + require('../assets/imgs/bg02.jpg') + ')'
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
                this.accountError = '请输入账号'
            } else {
                this.accountError = ''
            }
        },
        verifyPwd() {
            if (!this.pwd) {
                this.pwdError = '请输入密码'
            } else {
                this.pwdError = ''
            }
        },
        register(name, params) {
            this.$router.push({ name, params })
        },
        gotoPage() {

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
            const res = await login(`account=${this.account}&pwd=${this.pwd}`)
            console.log(res)
            if (res.code == 200){
                this.isShowLoading = true
                console.log(res)
                // 登陆成功 设置用户信息
                localStorage.setItem('userImg', 'https://avatars3.githubusercontent.com/u/22117876?s=460&v=4')
                localStorage.setItem('userName', res.session[0].name)
                localStorage.setItem('account', res.session[0].account)
                localStorage.setItem('role', res.session[0].role)
                localStorage.setItem('userId', res.session[0].id)
                // 登陆成功 假设这里是后台返回的 token
                localStorage.setItem('token', 'i_am_token')
                this.$router.push({path: this.redirect || '/'})
            } else {
                this.$Message.error('用户名或密码错误');
            }
        },
    },
}
</script>

<style>
.login-vue {
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #fff;
}

.login-vue .container {
    background: rgba(255, 255, 255, .5);
    width: 300px;
    text-align: center;
    border-radius: 10px;
    padding: 30px;
}

.login-vue .ivu-input {
    background-color: transparent;
    color: #fff;
    outline: #fff;
    border-color: #fff;
}

.login-vue ::-webkit-input-placeholder { /* WebKit, Blink, Edge */
    color: rgba(255, 255, 255, .8);
}

.login-vue :-moz-placeholder { /* Mozilla Firefox 4 to 18 */
    color: rgba(255, 255, 255, .8);
}

.login-vue ::-moz-placeholder { /* Mozilla Firefox 19+ */
    color: rgba(255, 255, 255, .8);
}

.login-vue :-ms-input-placeholder { /* Internet Explorer 10-11 */
    color: rgba(255, 255, 255, .8);
}

.login-vue .title {
    font-size: 16px;
    margin-bottom: 20px;
}

.login-vue .input-c {
    margin: auto;
    width: 200px;
}

.login-vue .error {
    color: red;
    text-align: left;
    margin: 5px auto;
    font-size: 12px;
    padding-left: 30px;
    height: 20px;
}

.login-vue .submit {
    width: 200px;
}

.login-vue .account {
    margin: 25px 23px 0 0;
    float: right;
    border-bottom: 1px #fff solid;
    font-size: 10px;
}

.login-vue .account span {
    cursor: pointer;
}

.login-vue .ivu-icon {
    color: #eee;
}

.login-vue .ivu-icon-ios-close-circle {
    color: #777;
}
</style>
