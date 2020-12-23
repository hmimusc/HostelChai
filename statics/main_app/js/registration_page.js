let date = new Date();
$('#dob').val(date.toISOString().split('T')[0]);

$('#user_type').onchange(function () {
    if($(this).val() === 'H'){
        $('#birth_certificate').attr('required', 'true');
        $('#nid').attr('required', true);
    }
    else {
        $('#birth_certificate').attr('required', 'false');
        $('#nid').attr('required', false);
    }
});
