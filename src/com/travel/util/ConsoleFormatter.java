package com.travel.util;

public class ConsoleFormatter {
    // ANSI Colors
    public static final String RESET = "\u001B[0m";
    public static final String BOLD = "\u001B[1m";
    public static final String RED = "\u001B[31m";
    public static final String GREEN = "\u001B[32m";
    public static final String YELLOW = "\u001B[33m";
    public static final String BLUE = "\u001B[34m";
    public static final String CYAN = "\u001B[36m";
    public static final String WHITE = "\u001B[37m";

    public static void printHeader(String title) {
        System.out.println();
        System.out.println(CYAN + BOLD + "==========================================================================================" + RESET);
        System.out.println(CYAN + BOLD + "   " + title.toUpperCase() + RESET);
        System.out.println(CYAN + BOLD + "==========================================================================================" + RESET);
    }

    public static void printSubHeader(String subtitle) {
        System.out.println(YELLOW + BOLD + "--- " + subtitle + " ---" + RESET);
    }

    public static void printSuccess(String message) {
        System.out.println(GREEN + BOLD + "[SUCCESS] " + message + RESET);
    }

    public static void printWarning(String message) {
        System.out.println(YELLOW + BOLD + "[WARNING] " + message + RESET);
    }

    public static void printError(String message) {
        System.out.println(RED + BOLD + "[ERROR] " + message + RESET);
    }

    public static void printInfo(String message) {
        System.out.println(BLUE + "[INFO] " + message + RESET);
    }

    public static void printDivider() {
        System.out.println("------------------------------------------------------------------------------------------");
    }
}
