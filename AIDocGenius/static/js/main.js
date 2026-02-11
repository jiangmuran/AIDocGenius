// AIDocGenius 前端 JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const operationType = document.getElementById('operationType');
    const targetLanguageContainer = document.getElementById('targetLanguageContainer');
    const outputFormatContainer = document.getElementById('outputFormatContainer');
    const batchOptions = document.getElementById('batchOptions');
    const batchTranslate = document.getElementById('batchTranslate');
    const batchConvert = document.getElementById('batchConvert');
    const batchZip = document.getElementById('batchZip');
    const processButton = document.getElementById('processButton');
    const resultCard = document.getElementById('resultCard');
    const resultContent = document.getElementById('resultContent');

    // 文件上传
    dropZone.addEventListener('click', () => fileInput.click());
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.backgroundColor = '#e9ecef';
    });
    dropZone.addEventListener('dragleave', () => {
        dropZone.style.backgroundColor = '#f8f9fa';
    });
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.style.backgroundColor = '#f8f9fa';
        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
        }
    });

    // 操作类型变化
    operationType.addEventListener('change', function() {
        const op = this.value;
        const isBatch = op === 'batch';
        batchOptions.style.display = isBatch ? 'block' : 'none';
        targetLanguageContainer.style.display = (op === 'translate' || (isBatch && batchTranslate.checked)) ? 'block' : 'none';
        outputFormatContainer.style.display = (op === 'convert' || (isBatch && batchConvert.checked)) ? 'block' : 'none';
        fileInput.multiple = isBatch;
    });

    batchTranslate.addEventListener('change', function() {
        if (operationType.value === 'batch') {
            targetLanguageContainer.style.display = this.checked ? 'block' : 'none';
        }
    });

    batchConvert.addEventListener('change', function() {
        if (operationType.value === 'batch') {
            outputFormatContainer.style.display = this.checked ? 'block' : 'none';
        }
    });

    // 处理文档
    processButton.addEventListener('click', async function() {
        const files = Array.from(fileInput.files);
        if (!files.length) {
            alert('请先选择文件');
            return;
        }

        const formData = new FormData();
        const op = operationType.value;
        if (op === 'batch') {
            files.forEach((f) => formData.append('files', f));
        } else {
            formData.append('file', files[0]);
        }

        let url = '';
        let params = {};

        switch (op) {
            case 'summarize':
                url = '/summarize';
                break;
            case 'translate':
                url = '/translate';
                params.target_language = document.getElementById('targetLanguage').value;
                break;
            case 'analyze':
                url = '/analyze';
                break;
            case 'convert':
                url = '/convert';
                params.output_format = document.getElementById('outputFormat').value;
                break;
            case 'batch':
                url = '/batch';
                params.operations = getBatchOperations();
                params.report = true;
                params.report_formats = 'json,md,csv';
                params.zip_output = batchZip.checked;
                if (batchTranslate.checked) {
                    params.target_language = document.getElementById('targetLanguage').value;
                }
                if (batchConvert.checked) {
                    params.output_format = document.getElementById('outputFormat').value;
                }
                break;
        }

        // 添加参数到 URL
        const queryString = new URLSearchParams(params).toString();
        if (queryString) {
            url += '?' + queryString;
        }

        processButton.disabled = true;
        processButton.textContent = '处理中...';

        try {
            const response = await fetch(url, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorText = await tryReadError(response);
                throw new Error(errorText || `HTTP error! status: ${response.status}`);
            }

            if (op === 'convert' || (op === 'batch' && batchZip.checked)) {
                const blob = await response.blob();
                const disposition = response.headers.get('Content-Disposition') || '';
                const match = disposition.match(/filename="?([^";]+)"?/i);
                const fallbackName = op === 'batch'
                    ? 'batch_results.zip'
                    : `converted.${document.getElementById('outputFormat').value}`;
                const fileName = match ? match[1] : fallbackName;
                displayResult({ blob, fileName }, op);
            } else {
                const data = await response.json();
                displayResult(data, op);
            }
        } catch (error) {
            resultCard.style.display = 'block';
            const alertDiv = document.createElement('div');
            alertDiv.className = 'alert alert-danger';
            alertDiv.textContent = `错误: ${error.message}`;
            resultContent.innerHTML = '';
            resultContent.appendChild(alertDiv);
        } finally {
            processButton.disabled = false;
            processButton.textContent = '处理文档';
        }
    });

    function displayResult(data, operation) {
        resultCard.style.display = 'block';
        resultContent.innerHTML = '';

        const payload = data && data.data ? data.data : data;
        const requestId = data && data.request_id ? data.request_id : null;

        const alertDiv = document.createElement('div');
        const strong = document.createElement('strong');

        switch (operation) {
            case 'summarize': {
                alertDiv.className = 'alert alert-success';
                strong.textContent = '摘要：';
                const p = document.createElement('p');
                p.textContent = payload.summary || '';
                alertDiv.appendChild(strong);
                alertDiv.appendChild(p);
                break;
            }
            case 'translate': {
                alertDiv.className = 'alert alert-info';
                strong.textContent = '翻译结果：';
                const p = document.createElement('p');
                p.textContent = payload.translation || '';
                alertDiv.appendChild(strong);
                alertDiv.appendChild(p);
                break;
            }
            case 'analyze': {
                alertDiv.className = 'alert alert-primary';
                strong.textContent = '分析结果：';
                const pre = document.createElement('pre');
                pre.textContent = JSON.stringify(payload, null, 2);
                alertDiv.appendChild(strong);
                alertDiv.appendChild(pre);
                break;
            }
            case 'convert': {
                alertDiv.className = 'alert alert-success';
                strong.textContent = '转换完成';
                alertDiv.appendChild(strong);
                if (data && data.blob) {
                    const url = URL.createObjectURL(data.blob);
                    const p = document.createElement('p');
                    const link = document.createElement('a');
                    link.href = url;
                    link.download = data.fileName;
                    link.textContent = '下载文件';
                    p.appendChild(link);
                    alertDiv.appendChild(p);
                }
                break;
            }
            case 'batch': {
                if (data && data.blob) {
                    alertDiv.className = 'alert alert-success';
                    strong.textContent = '批量处理完成';
                    alertDiv.appendChild(strong);
                    const url = URL.createObjectURL(data.blob);
                    const p = document.createElement('p');
                    const link = document.createElement('a');
                    link.href = url;
                    link.download = data.fileName;
                    link.textContent = '下载结果';
                    p.appendChild(link);
                    alertDiv.appendChild(p);
                } else {
                    alertDiv.className = 'alert alert-primary';
                    strong.textContent = '批量报告：';
                    const pre = document.createElement('pre');
                    pre.textContent = JSON.stringify(payload, null, 2);
                    alertDiv.appendChild(strong);
                    alertDiv.appendChild(pre);
                }
                break;
            }
        }

        resultContent.appendChild(alertDiv);

        if (requestId) {
            const meta = document.createElement('div');
            meta.className = 'text-muted small mt-2';
            meta.textContent = `request_id: ${requestId}`;
            resultContent.appendChild(meta);
        }
    }

    function getBatchOperations() {
        const ops = [];
        if (document.getElementById('batchSummarize').checked) ops.push('summarize');
        if (document.getElementById('batchTranslate').checked) ops.push('translate');
        if (document.getElementById('batchAnalyze').checked) ops.push('analyze');
        if (document.getElementById('batchConvert').checked) ops.push('convert');
        return ops.join(',');
    }

    async function tryReadError(response) {
        const contentType = response.headers.get('Content-Type') || '';
        if (contentType.includes('application/json')) {
            const data = await response.json();
            if (data && data.error && data.error.message) {
                return `${data.error.message} (${data.request_id || 'no-id'})`;
            }
        }
        return null;
    }
});
