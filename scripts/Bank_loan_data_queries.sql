CREATE VIEW bank_loan_db.cleaned_loan_view AS
SELECT 
    address_state,
    emp_length,
    grade,
    home_ownership,
    purpose,
    term,
    verification_status,
    annual_income,
    dti,
    installment,
    int_rate,
    loan_amount,
    total_acc,
    -- Creating the Target Variable for Machine Learning
    CASE 
        WHEN loan_status = 'Charged Off' THEN 1 
        ELSE 0 
    END AS is_bad_loan
FROM 
    bank_loan_db.raw_loan_data
WHERE 
    annual_income IS NOT NULL 
    AND dti IS NOT NULL
    AND emp_length IS NOT NULL;
