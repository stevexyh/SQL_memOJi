Dropzone.options.fileDropzoneCSV = {
    acceptedFiles: ".csv",
    addRemoveLinks: true,
    method: "post",
    filesizeBase: 1024,
    paramName: "file", // The name that will be used to transfer the file
    maxFilesize: 5, // MB
    dictResponseError: "上传失败",
    dictRemoveFile: "删除文件",
    dictCancelUpload: "dictCancelUpload",
    dictFileTooBig: "文件大小: {{filesize}} MB\n最大限制: {{maxFilesize}} MB",
}
// alert("Dropzone.JS加载正常\nRemove Before Flight");
