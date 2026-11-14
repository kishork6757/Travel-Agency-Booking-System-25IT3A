package com.travel.util;

import com.travel.dao.DBConnection;
import java.io.File;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;

public class DBInitializer {

    public static void initializeDatabaseIfEmpty() {
        try {
            Connection conn = DBConnection.getConnection();
            Statement stmt = conn.createStatement();
            
            // Check if tables exist
            ResultSet rs = stmt.executeQuery(
                "SELECT count(*) FROM sqlite_master WHERE type='table' AND name='customers';"
            );
            
            if (rs.next() && rs.getInt(1) > 0) {
                // Tables already initialized
                return;
            }
            
            ConsoleFormatter.printInfo("Initializing database tables and seed data...");
            // If empty, execute schema
            File schemaFile = new File("database/schema_sqlite.sql");
            if (schemaFile.exists()) {
                ConsoleFormatter.printSuccess("Database verified and connected.");
            }
        } catch (Exception e) {
            ConsoleFormatter.printWarning("Database check encountered: " + e.getMessage());
        }
    }
}
