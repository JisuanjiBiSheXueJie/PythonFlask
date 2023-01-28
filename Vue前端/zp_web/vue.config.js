module.exports = {
    lintOnSave:false,//关闭eslint
    devServer: {
        port: 8099, // 端口号
        https: false,
        open: false,
        proxy: {
            '/api': {
                target: 'http://127.0.0.1:5000/', // 对应自己的接口
                changeOrigin: true,
                ws: true,
                pathRewrite: {
                    '^/api': '',
                },
            },
        },
    },
    publicPath: './',
}
