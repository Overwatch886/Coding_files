extern printf
global main

section .data
    msg db "Hello, World!", 0   ; Null-terminated string

section .text
main:
    sub rsp, 40                 ; Reserve 32 bytes shadow space + 8 bytes alignment
    lea rcx, [rel msg]          ; Load address of msg into RCX (1st argument)
    call printf                 ; Call printf
    add rsp, 40                 ; Clean up the stack
    
    mov eax, 0                  ; Return 0
    ret