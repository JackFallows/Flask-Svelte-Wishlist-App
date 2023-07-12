const { src, dest, series, watch } = require("gulp");
const { exec } = require("child_process");

function processCallback(error, stdout, stderr) {
    if (error) {
        console.error(`exec error: ${error}`);
        return;
    }

    if (stdout) {
        console.log(`stdout: ${stdout}`);
    }

    if (stderr) {
        console.error(`stderr: ${stderr}`);
    }
}

function validateTs() {
    return exec("npm run validate", processCallback)
}

function build() {
    return exec("npm run build-debug", processCallback);
}

function copyLibraryContent() {
    return src([
        "./node_modules/bootstrap/dist/css/bootstrap.min.css",
        "./node_modules/bootstrap/dist/js/bootstrap.min.js",
        "./node_modules/@popperjs/core/dist/umd/popper.min.js"
    ])
    .pipe(dest("./public/library_content"));
}

function buildProject() {
    watch("./src/**/*", { ignoreInitial: false }, series(validateTs, build));
}

exports.default = series(copyLibraryContent, buildProject);
