module.exports = {
    runtimeCompiler: true,
    publicPath: process.env.NODE_ENV === "production" ? "/static/dist" : "/",
    outputDir: "../static/dist"
};
