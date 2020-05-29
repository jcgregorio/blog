/*
blowfish_test.c:  Test file for blowfish.c

Copyright (C) 1997 by Paul Kocher

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.
This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.
You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
*/

#include <stdio.h>
#include <math.h>
#include "blowfish.h"

// p - Pointer to a 64-bit block of memory
// output - Pointer to a string buffer that will be concatenated with
//     the output of the encryption. The output will be formatted in hex.
void encrypt(BLOWFISH_CTX * ctx, char a, char b, char c, char d, char * output) {
    unsigned long L, R;
    char buf[20];
    L = a + (b << 16);
    R = c + (d << 16);
    Blowfish_Encrypt(ctx, &L, &R);
    sprintf (buf, "%08lX%08lX", L, R);
    strcat(output, buf);
}

void decrypt(BLOWFISH_CTX * ctx, unsigned char * p, char * output) {
    unsigned long L, R;
    char buf[9];
    buf[8] = 0;
    strncpy(buf, p, 8);
    sscanf(buf, "%08x", &L);
    strncpy(buf, p+8, 8);
    sscanf(buf, "%08x", &R);
    Blowfish_Decrypt(ctx, &L, &R);
    char s[3];
    s[0] = 0xFFFF & L;
    s[1] = L >> 16;
    s[2] = 0;
    strcat(output, s);
    s[0] = 0xFFFF & R;
    s[1] = R >> 16;
    strcat(output, s);
}

void main(void) {
    unsigned long L = 1, R = 2;
    int i;
    BLOWFISH_CTX ctx;

    Blowfish_Init (&ctx, (unsigned char*)"TESTKEY", 7);
    Blowfish_Encrypt(&ctx, &L, &R);
    if (L == 0xDF333FD2L && R == 0x30A71BB4L)
        printf("Test encryption OK.\n");
    else
        printf("Test encryption failed.\n");
    Blowfish_Decrypt(&ctx, &L, &R);
    if (L == 1 && R == 2)
        printf("Test decryption OK.\n");
    else
        printf("Test decryption failed.\n");

    Blowfish_Init (&ctx, (unsigned char*)"TESTKEY", 7);

    char message[2048];
    strcpy(message, "This is a <b>Blowfish</b> encrypted message.");
    printf("\nBefore   : ");
    int length = strlen(message);
    if (length & 0x01) {
        length++;
    }
    for (i=0; i<length; i++) {
        printf("%02X", message[i]);
    }

    unsigned char * p = message;
    char output[8192];
    output[0] = 0;
    for (i=0; i<length; i+=4) {
        encrypt(&ctx, *p, *(p+1), *(p+2), *(p+3), output);
        p += 4; 
    }
    printf("\nEncrypted: %s\n", output);

    Blowfish_Init (&ctx, (unsigned char*)"TESTKEY", 7);
    p = output;
    printf ("\nDecrypted\n");
    char dec_output[1024];
    dec_output[0] = 0;
    for (i=0; i<length*4; i+=16) {
        decrypt(&ctx, p, dec_output);
        p += 16;
    } 
    printf("%s\n", dec_output);
}

