$(document).ready(function () {
    $(".datatable").DataTable({
        lengthMenu: [5, 10, 25, 50],
        pageLength: 5,
        info: "aaa _START_ to _END_ of _TOTAL_ entries",
        columns: [
            { orderable: false },
            { orderable: true },
            { orderable: true },
            { orderable: true },
            { orderable: true },
            { orderable: true },
            { orderable: true },
            { orderable: false },
        ],
        order: [[1, "asc"]],
        language: {
            paginate: {
                previous: "<i class='mdi mdi-chevron-left'>",
                next: "<i class='mdi mdi-chevron-right'>",
                first: "首页",
                last: "末页",
            },
            processing: "处理中...",
            lengthMenu: "显示 _MENU_ 项结果",
            zeroRecords: "没有匹配结果",
            info: "显示第 _START_ 至 _END_ 项结果，共 _TOTAL_ 项",
            infoEmpty: "显示第 0 至 0 项结果，共 0 项",
            infoFiltered: "(由 _MAX_ 项结果过滤)",
            search: "搜索:",
            emptyTable: "表中数据为空",
            aria: {
                sortAscending: ": 以升序排列此列",
                sortDescending: ": 以降序排列此列",
            },
            autoFill: {
                cancel: "取消",
                fill: "用 <i>%d</i> 填充所有单元格",
                fillHorizontal: "水平填充单元格",
                fillVertical: "垂直填充单元格",
                info: "自动填充示例",
            },
            buttons: {
                collection:
                    '集合 <span class="ui-button-icon-primary ui-icon ui-icon-triangle-1-s"></span>',
                colvis: "列可见性",
                colvisRestore: "恢复列可见性",
                copy: "复制",
                copyKeys:
                    "按 ctrl 或者 u2318 + C 将表数据复制到剪贴板。<br /><br />要取消，请单击此消息或按Escape键。",
                copyTitle: "复制到剪贴板",
                csv: "CSV",
                excel: "Excel",
                pdf: "PDF",
                copySuccess: {
                    1: "已将 1 行复制到剪贴板",
                    _: "已将 %d 行复制到剪贴板",
                },
                pageLength: {
                    "-1": "显示所有行",
                    1: "显示 1 行",
                    _: "显示 %d 行",
                },
                print: "打印",
            },
            searchBuilder: {
                add: "添加搜索条件",
                button: {
                    0: "搜索生成器",
                    _: "搜索生成器 (%d)",
                },
                clearAll: "全部清除",
                condition: "条件",
                data: "数据",
                deleteTitle: "删除过滤规则",
                leftTitle: "Outdent 条件",
                logicAnd: "And",
                logicOr: "Or",
                rightTitle: "Indent 条件",
                title: {
                    0: "搜索生成器",
                    _: "搜索生成器 (%d)",
                },
                value: "值",
                conditions: {
                    date: {
                        after: "日期条件查询为after条件名称：大于",
                        before: "日期条件查询为before条件名称：小于",
                        between:
                            "日期条件查询为between条件名称：介于2个日期之间",
                        empty: "日期条件查询为empty条件名称：日期为空",
                        equals: "日期条件查询为equals条件名称：等于",
                        notBetween:
                            "日期条件查询为notBetween条件名称：不介于2个日期之间",
                        notEmpty: "日期条件查询为notEmpty条件名称：日期不为空",
                    },
                    string: {
                        contains: "文本包含",
                        empty: "文本为空",
                        endsWith: "文本以某某结尾",
                        equals: "文本等于",
                        not: "文本不等于",
                        notEmpty: "文本不为空",
                        startsWith: "文本从某某开始",
                    },
                },
            },
            searchPanes: {
                collapse: {
                    0: "搜索栏",
                    _: "搜索栏（%d）",
                },
                title: "应用的过滤器 - %d",
                clearMessage: "全部清除",
                count: "计数",
                countFiltered: "过滤计数",
                emptyPanes: "没有搜索栏",
                loadMessage: "正在加载搜索栏",
            },
            searchPlaceholder: "请输入查询关键字",
            select: {
                _: "选择了%d行",
                cells: {
                    1: "选择了1个单元格",
                    _: "选择了%d个单元格",
                },
                columns: {
                    1: "选择了1列",
                    _: "选择了%d列",
                },
                0: "没有选中数据行的文字说明",
                1: "选中一行的文字说明",
                rows: {
                    1: "被选中一行的说明",
                    _: "被选中多行的说明",
                },
            },
            decimal: "",
            infoPostFix: "",
            infoThousands: "千分数分隔符，默认值是英文逗号",
            loadingRecords: "数据加载提示信息，例如：数据加载中...",
            thousands: "千位分隔符，默认值是英文逗号",
        },
        drawCallback: function () {
            $(".dataTables_paginate > .pagination").addClass(
                "pagination-rounded"
            );
        },
    });
});

Dropzone.options.fileDropzoneStud = {
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
alert("Dropzone.JS加载正常\nRemove Before Flight");
