package com.travel.dao;

import java.io.File;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DBConnection {
    private static Connection connection = null;

    // Resolve relative path to database/travel_agency.db
    private static String getDatabasePath() {
        File dbFile = new File("database/travel_agency.db");
        if (!dbFile.exists()) {
            // Check if running from root or child folder
            File parentDb = new File("../database/travel_agency.db");
            if (parentDb.exists()) {
                return parentDb.getAbsolutePath();
            }
        }
        return dbFile.getAbsolutePath();
    }

    public static synchronized Connection getConnection() throws SQLException {
        if (connection == null || connection.isClosed()) {
            try {
                // Load SQLite JDBC Driver
                Class.forName("org.sqlite.JDBC");
                String dbPath = getDatabasePath();
                String url = "jdbc:sqlite:" + dbPath;
                connection = DriverManager.getConnection(url);
                
                // Enable SQLite Foreign Key constraints
                connection.createStatement().execute("PRAGMA foreign_keys = ON;");
            } catch (ClassNotFoundException e) {
                System.err.println("[ERROR] SQLite JDBC Driver not found in classpath: " + e.getMessage());
                throw new SQLException("SQLite JDBC Driver missing.", e);
            }
        }
        return connection;
    }

    public static void closeConnection() {
        if (connection != null) {
            try {
                if (!connection.isClosed()) {
                    connection.close();
                }
            } catch (SQLException e) {
                System.err.println("[WARN] Failed to close database connection: " + e.getMessage());
            }
        }
    }
}
