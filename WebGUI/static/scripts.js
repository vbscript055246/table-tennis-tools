$(document).ready(function() {

    $('#product_name').change(function() {
        var selectedName = $(this).val();
        $('#submit_button').prop('disabled', selectedName === '' || selectedName === null);
    });

    // 如果需要取消選擇，則設置為禁用狀態
    $('#product_name').on('select2:clear', function() {
        $('#submit_button').prop('disabled', true);
    });

    $('#product_type').on('select2:clear', function() {
        $('#submit_button').prop('disabled', true);
    });

    $('#product_type').select2({
        placeholder: "請選擇產品類型",
        allowClear: true,
        tags: false
    });

    $('#product_name').select2({
        placeholder: "請先選擇產品類型",
        allowClear: true,
        tags: false
    });

    // 攔截表單提交，將資料封裝為物件傳送到後端
    $('#equipment_form').submit(function(e) {
        e.preventDefault(); // 防止表單的默認提交行為
        var selectedType = $('#product_type').val();
        var productName = $('#product_name').val();
        var formData = {
            product_type: selectedType,
            product_name: productName
        };
        console.log('formData:', formData);
        // 根據不同的產品類型收集資料
        if (selectedType === 'blade') {
            formData['blade_speed'] = $('input[name="blade_speed"]:checked').val();
            formData['blade_control'] = $('input[name="blade_control"]:checked').val();
            formData['blade_sitffness'] = $('input[name="blade_sitffness"]:checked').val();
            formData['blade_hardness'] = $('input[name="blade_hardness"]:checked').val();

        } else if (selectedType === 'rubber') {
            formData['rubber_speed'] = $('input[name="rubber_speed"]:checked').val();
            formData['rubber_spin'] = $('input[name="rubber_spin"]:checked').val();
            formData['rubber_control'] = $('input[name="rubber_control"]:checked').val();
            formData['rubber_tackiness'] = $('input[name="rubber_tackiness"]:checked').val();
            formData['rubber_hardness'] = $('input[name="rubber_hardness"]:checked').val();
            formData['rubber_gears'] = $('input[name="rubber_gears"]:checked').val();
            formData['rubber_angle'] = $('input[name="rubber_angle"]:checked').val();

        }
        else if (selectedType === 'pips') {
            formData['pips_speed'] = $('input[name="pips_speed"]:checked').val();
            formData['pips_spin'] = $('input[name="pips_spin"]:checked').val();
            formData['pips_control'] = $('input[name="pips_control"]:checked').val();
            formData['pips_deception'] = $('input[name="pips_deception"]:checked').val();
            formData['pips_reversal'] = $('input[name="pips_reversal"]:checked').val();
            formData['pips_hardness'] = $('input[name="pips_hardness"]:checked').val();
        }

        // 使用 Ajax 將封裝的資料傳送到 Flask 後端
        $.ajax({
            url: '/search',
            type: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(formData),
            success: function(response) {
                //console.log('Server Response:', response);  // 檢查伺服器回應內容

                // 確認 response 是否有內容
                if (response.length === 0) {
                    alert('沒有資料可顯示');
                    return;
                }

                // 根據 selectedType 設置固定的表頭欄位名稱與順序
                var columns;
                if (selectedType === 'blade') {
                    columns = ['Name', 'Speed', 'Control', 'Sitffness', 'Hardness', 'Total Std', 'Price'];
                } else if (selectedType === 'rubber') {
                    columns = ['Name', 'Speed', 'Spin', 'Control', 'Tackiness', 'Hardness', 'Gears', 'Angle', 'Total Std', 'Price', 'Durability'];
                } else if (selectedType === 'pips') {
                    columns = ['Name', 'Speed', 'Spin', 'Control', 'Deception', 'Reversal', 'Hardness', 'Total Std', 'Price', 'Durability'];
                } else {
                    alert('未知的產品類型');
                    return;
                }

                // 清空現有的結果表格，包括表頭和表格內容
                $('#results-table thead').empty();
                $('#results-table tbody').empty();

                // 動態生成表格的表頭，第一欄添加 "序號"
                var headerRow = '<tr><th></th>';
                columns.forEach(function(column) {
                    headerRow += '<th>' + column + '</th>';
                });
                headerRow += '</tr>';
                $('#results-table thead').append(headerRow);

                // 動態生成表格的行，將每個物件的屬性插入表格中，並加上流水號
                response.forEach(function(item, index) {
                    var row = '<tr>';
                    row += '<td>' + (index + 1) + '</td>';  // 添加流水號（從 1 開始）
                    columns.forEach(function(column) {
                        row += '<td>' + (item[column] !== undefined ? item[column] : '') + '</td>';
                    });
                    row += '</tr>';
                    $('#results-table tbody').append(row);
                });
            },
            error: function(err) {
                console.log('Error:', err);
            }
        });
    });


    // 當產品類型選擇時，觸發 Ajax 請求獲取相應的產品名稱
    $('#product_type').change(function() {
        var selectedType = $(this).val();

        if (selectedType) {
            // 發送 Ajax 請求到 Flask 後端，根據產品類型獲取對應的產品名稱
            $.ajax({
                url: '/get_product_names',
                type: 'GET',
                data: { product_type: selectedType },
                success: function(data) {
                    // 清空之前的選項
                    $('#product_name').empty();

                    // 將新的選項加入第二個下拉選單
                    $('#product_name').append('<option value="" disabled selected>請選擇產品名稱</option>');
                    data.forEach(function(item) {
                        $('#product_name').append('<option value="' + item + '">' + item + '</option>');
                    });
                    // 啟用第二個下拉選單
                    $('#product_name').prop('disabled', false).select2({
                        placeholder: "請選擇產品名稱",
                        allowClear: true
                    });
                }
            });
        } else {
            // 如果未選擇產品類型，禁用產品名稱選單
            $('#product_name').empty().append('<option value="" disabled selected>請先選擇產品類型</option>').prop('disabled', true);
        }
    });

    $('#product_type').change(function() {
        var selectedType = $(this).val();
        var dynamicFields = $('#right-side');
        dynamicFields.empty();  // 清空原有的欄位

        if (selectedType === 'blade') {
            // 生成 Blade 的欄位
            dynamicFields.append(`
                <div class="field-group">
                    <label for="blade_speed">Speed:</label>
                    <div class="radio-options">
                        <label><input type="radio" name="blade_speed" value="1"> > </label>
                        <label><input type="radio" name="blade_speed" value="2"> = </label>
                        <label><input type="radio" name="blade_speed" value="3"> < </label>
                        <label><input type="radio" name="blade_speed" value="4" checked> O </label>
                        <label><input type="radio" name="blade_speed" value="5"> X </label>
                    </div>
                </div>
            `);
            dynamicFields.append(`
                <div class="field-group">
                    <label for="blade_control">Control:</label>
                    <div class="radio-options">
                        <label><input type="radio" name="blade_control" value="1"> > </label>
                        <label><input type="radio" name="blade_control" value="2"> = </label>
                        <label><input type="radio" name="blade_control" value="3"> < </label>
                        <label><input type="radio" name="blade_control" value="4" checked> O </label>
                        <label><input type="radio" name="blade_control" value="5"> X </label>
                    </div>
                </div>
            `);

            dynamicFields.append(`
                <div class="field-group">
                    <label for="blade_sitffness">Sitffness:</label>
                    <div class="radio-options">
                        <label><input type="radio" name="blade_sitffness" value="1"> > </label>
                        <label><input type="radio" name="blade_sitffness" value="2"> = </label>
                        <label><input type="radio" name="blade_sitffness" value="3"> < </label>
                        <label><input type="radio" name="blade_sitffness" value="4" checked> O </label>
                        <label><input type="radio" name="blade_sitffness" value="5"> X </label>
                    </div>
                </div>
            `);

            dynamicFields.append(`
                <div class="field-group">
                    <label for="blade_hardness">Hardness:</label>
                    <div class="radio-options">
                        <label><input type="radio" name="blade_hardness" value="1"> > </label>
                        <label><input type="radio" name="blade_hardness" value="2"> = </label>
                        <label><input type="radio" name="blade_hardness" value="3"> < </label>
                        <label><input type="radio" name="blade_hardness" value="4" checked> O </label>
                        <label><input type="radio" name="blade_hardness" value="5"> X </label>
                    </div>
                </div>
            `);

        } else if (selectedType === 'rubber') {

            dynamicFields.append(`
                <div class="field-group">
                    <label for="rubber_speed">Speed:</label>
                    <div class="radio-options">
                        <label><input type="radio" name="rubber_speed" value="1"> > </label>
                        <label><input type="radio" name="rubber_speed" value="2"> = </label>
                        <label><input type="radio" name="rubber_speed" value="3"> < </label>
                        <label><input type="radio" name="rubber_speed" value="4" checked> O </label>
                        <label><input type="radio" name="rubber_speed" value="5"> X </label>
                    </div>
                </div>
            `);
            dynamicFields.append(`
                <div class="field-group">
                    <label for="rubber_spin">Spin:</label>
                    <div class="radio-options">
                        <label><input type="radio" name="rubber_spin" value="1"> > </label>
                        <label><input type="radio" name="rubber_spin" value="2"> = </label>
                        <label><input type="radio" name="rubber_spin" value="3"> < </label>
                        <label><input type="radio" name="rubber_spin" value="4" checked> O </label>
                        <label><input type="radio" name="rubber_spin" value="5"> X </label>
                    </div>
                </div>
            `);
            dynamicFields.append(`
                <div class="field-group">
                    <label for="rubber_control">Control:</label>
                    <div class="radio-options">
                        <label><input type="radio" name="rubber_control" value="1"> > </label>
                        <label><input type="radio" name="rubber_control" value="2"> = </label>
                        <label><input type="radio" name="rubber_control" value="3"> < </label>
                        <label><input type="radio" name="rubber_control" value="4" checked> O </label>
                        <label><input type="radio" name="rubber_control" value="5"> X </label>
                    </div>
                </div>
            `);
            dynamicFields.append(`
                <div class="field-group">
                    <label for="rubber_tackiness">Tackiness:</label>
                    <div class="radio-options">
                        <label><input type="radio" name="rubber_tackiness" value="1"> > </label>
                        <label><input type="radio" name="rubber_tackiness" value="2"> = </label>
                        <label><input type="radio" name="rubber_tackiness" value="3"> < </label>
                        <label><input type="radio" name="rubber_tackiness" value="4" checked> O </label>
                        <label><input type="radio" name="rubber_tackiness" value="5"> X </label>
                    </div>
                </div>
            `);
            dynamicFields.append(`
                <div class="field-group">
                    <label for="rubber_hardness">Hardness:</label>
                    <div class="radio-options">
                        <label><input type="radio" name="rubber_hardness" value="1"> > </label>
                        <label><input type="radio" name="rubber_hardness" value="2"> = </label>
                        <label><input type="radio" name="rubber_hardness" value="3"> < </label>
                        <label><input type="radio" name="rubber_hardness" value="4" checked> O </label>
                        <label><input type="radio" name="rubber_hardness" value="5"> X </label>
                    </div>
                </div>
            `);
            dynamicFields.append(`
                <div class="field-group">
                    <label for="rubber_gears">Gears:</label>
                    <div class="radio-options">
                        <label><input type="radio" name="rubber_gears" value="1"> > </label>
                        <label><input type="radio" name="rubber_gears" value="2"> = </label>
                        <label><input type="radio" name="rubber_gears" value="3"> < </label>
                        <label><input type="radio" name="rubber_gears" value="4" checked> O </label>
                        <label><input type="radio" name="rubber_gears" value="5"> X </label>
                    </div>
                </div>
            `);
            dynamicFields.append(`
                <div class="field-group">
                    <label for="rubber_angle">Angle:</label>
                    <div class="radio-options">
                        <label><input type="radio" name="rubber_angle" value="1"> > </label>
                        <label><input type="radio" name="rubber_angle" value="2"> = </label>
                        <label><input type="radio" name="rubber_angle" value="3"> < </label>
                        <label><input type="radio" name="rubber_angle" value="4" checked> O </label>
                        <label><input type="radio" name="rubber_angle" value="5"> X </label>
                    </div>
                </div>
            `);
        } else if (selectedType === 'pips') {

            dynamicFields.append(`
                <div class="field-group">
                    <label for="pips_speed">Speed:</label>
                    <div class="radio-options">
                        <label><input type="radio" name="pips_speed" value="1"> > </label>
                        <label><input type="radio" name="pips_speed" value="2"> = </label>
                        <label><input type="radio" name="pips_speed" value="3"> < </label>
                        <label><input type="radio" name="pips_speed" value="4" checked> O </label>
                        <label><input type="radio" name="pips_speed" value="5"> X </label>
                    </div>
                </div>
            `);
            dynamicFields.append(`
                <div class="field-group">
                    <label for="pips_spin">Spin:</label>
                    <div class="radio-options">
                        <label><input type="radio" name="pips_spin" value="1"> > </label>
                        <label><input type="radio" name="pips_spin" value="2"> = </label>
                        <label><input type="radio" name="pips_spin" value="3"> < </label>
                        <label><input type="radio" name="pips_spin" value="4" checked> O </label>
                        <label><input type="radio" name="pips_spin" value="5"> X </label>
                    </div>
                </div>
            `);
            dynamicFields.append(`
                <div class="field-group">
                    <label for="pips_control">Control:</label>
                    <div class="radio-options">
                        <label><input type="radio" name="pips_control" value="1"> > </label>
                        <label><input type="radio" name="pips_control" value="2"> = </label>
                        <label><input type="radio" name="pips_control" value="3"> < </label>
                        <label><input type="radio" name="pips_control" value="4" checked> O </label>
                        <label><input type="radio" name="pips_control" value="5"> X </label>
                    </div>
                </div>
            `);
            dynamicFields.append(`
                <div class="field-group">
                    <label for="pips_deception">Deception:</label>
                    <div class="radio-options">
                        <label><input type="radio" name="pips_deception" value="1"> > </label>
                        <label><input type="radio" name="pips_deception" value="2"> = </label>
                        <label><input type="radio" name="pips_deception" value="3"> < </label>
                        <label><input type="radio" name="pips_deception" value="4" checked> O </label>
                        <label><input type="radio" name="pips_deception" value="5"> X </label>
                    </div>
                </div>
            `);
            dynamicFields.append(`
                <div class="field-group">
                    <label for="pips_reversal">Reversal:</label>
                    <div class="radio-options">
                        <label><input type="radio" name="pips_reversal" value="1"> > </label>
                        <label><input type="radio" name="pips_reversal" value="2"> = </label>
                        <label><input type="radio" name="pips_reversal" value="3"> < </label>
                        <label><input type="radio" name="pips_reversal" value="4" checked> O </label>
                        <label><input type="radio" name="pips_reversal" value="5"> X </label>
                    </div>
                </div>
            `);
            dynamicFields.append(`
                <div class="field-group">
                    <label for="pips_hardness">Hardness:</label>
                    <div class="radio-options">
                        <label><input type="radio" name="pips_hardness" value="1"> > </label>
                        <label><input type="radio" name="pips_hardness" value="2"> = </label>
                        <label><input type="radio" name="pips_hardness" value="3"> < </label>
                        <label><input type="radio" name="pips_hardness" value="4" checked> O </label>
                        <label><input type="radio" name="pips_hardness" value="5"> X </label>
                    </div>
                </div>
            `);
        }
    });
});