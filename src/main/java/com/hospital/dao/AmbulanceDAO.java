package com.hospital.dao;

import com.hospital.model.Ambulance;
import com.hospital.util.DatabaseUtil;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

/**
 * Data Access Object for Ambulance entity
 */
public class AmbulanceDAO {

    /**
     * Get all ambulances from the database
     * @return List of ambulances
     */
    public List<Ambulance> getAllAmbulances() {
        List<Ambulance> ambulances = new ArrayList<>();
        Connection conn = null;
        PreparedStatement stmt = null;
        ResultSet rs = null;

        try {
            conn = DatabaseUtil.getConnection();
            String sql = "SELECT * FROM ambulances";
            stmt = conn.prepareStatement(sql);
            rs = stmt.executeQuery();

            while (rs.next()) {
                Ambulance amb = new Ambulance(
                    rs.getString("ambulance_id"),
                    rs.getString("driver_name"),
                    rs.getString("driver_phone"),
                    rs.getString("plate_number")
                );
                amb.setAvailable(rs.getBoolean("is_available"));
                ambulances.add(amb);
            }
        } catch (SQLException e) {
            System.err.println("Error getting ambulances: " + e.getMessage());
        } finally {
            try {
                if (rs != null) rs.close();
                if (stmt != null) stmt.close();
            } catch (SQLException e) {
                System.err.println("Error closing resources: " + e.getMessage());
            }
            DatabaseUtil.closeConnection(conn);
        }

        return ambulances;
    }

    /**
     * Add an ambulance to the database
     * @param amb Ambulance to add
     * @return true if successful, false otherwise
     */
    public boolean addAmbulance(Ambulance amb) {
        Connection conn = null;
        PreparedStatement stmt = null;

        try {
            conn = DatabaseUtil.getConnection();
            String sql = "INSERT INTO ambulances (ambulance_id, driver_name, driver_phone, plate_number, is_available) VALUES (?, ?, ?, ?, ?)";
            stmt = conn.prepareStatement(sql);
            stmt.setString(1, amb.getAmbulanceId());
            stmt.setString(2, amb.getDriverName());
            stmt.setString(3, amb.getDriverPhone());
            stmt.setString(4, amb.getPlateNumber());
            stmt.setBoolean(5, amb.isAvailable());

            int rowsAffected = stmt.executeUpdate();
            return rowsAffected > 0;
        } catch (SQLException e) {
            System.err.println("Error adding ambulance: " + e.getMessage());
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

    /**
     * Update ambulance availability
     * @param ambulanceId Ambulance ID
     * @param available New availability status
     * @return true if successful, false otherwise
     */
    public boolean updateAvailability(String ambulanceId, boolean available) {
        Connection conn = null;
        PreparedStatement stmt = null;

        try {
            conn = DatabaseUtil.getConnection();
            String sql = "UPDATE ambulances SET is_available = ? WHERE ambulance_id = ?";
            stmt = conn.prepareStatement(sql);
            stmt.setBoolean(1, available);
            stmt.setString(2, ambulanceId);

            int rowsAffected = stmt.executeUpdate();
            return rowsAffected > 0;
        } catch (SQLException e) {
            System.err.println("Error updating ambulance availability: " + e.getMessage());
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
