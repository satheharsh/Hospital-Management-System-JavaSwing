package com.hospital.dao;

import com.hospital.model.Department;
import com.hospital.util.DatabaseUtil;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

/**
 * Data Access Object for Department entity
 */
public class DepartmentDAO {

    /**
     * Get all departments from the database
     * @return List of departments
     */
    public List<Department> getAllDepartments() {
        List<Department> departments = new ArrayList<>();
        Connection conn = null;
        PreparedStatement stmt = null;
        ResultSet rs = null;

        try {
            conn = DatabaseUtil.getConnection();
            String sql = "SELECT * FROM departments";
            stmt = conn.prepareStatement(sql);
            rs = stmt.executeQuery();

            while (rs.next()) {
                Department dept = new Department(
                    rs.getString("name"),
                    rs.getString("phone_number")
                );
                departments.add(dept);
            }
        } catch (SQLException e) {
            System.err.println("Error getting departments: " + e.getMessage());
        } finally {
            try {
                if (rs != null) rs.close();
                if (stmt != null) stmt.close();
            } catch (SQLException e) {
                System.err.println("Error closing resources: " + e.getMessage());
            }
            DatabaseUtil.closeConnection(conn);
        }

        return departments;
    }

    /**
     * Add a department to the database
     * @param dept Department to add
     * @return true if successful, false otherwise
     */
    public boolean addDepartment(Department dept) {
        Connection conn = null;
        PreparedStatement stmt = null;

        try {
            conn = DatabaseUtil.getConnection();
            String sql = "INSERT INTO departments (name, phone_number) VALUES (?, ?)";
            stmt = conn.prepareStatement(sql);
            stmt.setString(1, dept.getName());
            stmt.setString(2, dept.getPhoneNumber());

            int rowsAffected = stmt.executeUpdate();
            return rowsAffected > 0;
        } catch (SQLException e) {
            System.err.println("Error adding department: " + e.getMessage());
            return false;
        } finally {
            try {
                if (stmt != null) stmt.close();
            } catch (SQLException e) {
                System.err.println("Error closing statement: " + e.getMessage());
            }
            DatabaseUtil.closeConnection(conn);
        }
    }
}
