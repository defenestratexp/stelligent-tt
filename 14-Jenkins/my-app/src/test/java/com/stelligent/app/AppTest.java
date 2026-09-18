package com.stelligent.app;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

/**
 * Unit test for simple App.
 */
class AppTest {
    @Test
    void greetsTheWorld() {
        assertEquals("Hello World!", App.greeting());
    }
}
