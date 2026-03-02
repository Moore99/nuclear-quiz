package com.nuclearmotd.quiz.data.prefs

import kotlinx.cinterop.*
import platform.Foundation.*
import platform.Security.*
import platform.posix.memcpy

/**
 * iOS token storage backed by the system Keychain.
 *
 * Each value is stored as a separate generic password item keyed by account name
 * under the service "com.nuclearmotd.quiz". Items survive app reinstalls when
 * iCloud Keychain sync is enabled, and are isolated to this app's entitlements.
 */
@OptIn(ExperimentalForeignApi::class)
class IosTokenStore : TokenStore {

    private val service = "com.nuclearmotd.quiz"

    override fun saveToken(token: String, username: String, userId: Int) {
        write(KEY_TOKEN, token)
        write(KEY_USERNAME, username)
        write(KEY_USER_ID, userId.toString())
    }

    override fun getToken(): String? = read(KEY_TOKEN)
    override fun getUsername(): String? = read(KEY_USERNAME)
    override fun getUserId(): Int = read(KEY_USER_ID)?.toIntOrNull() ?: 0
    override fun isLoggedIn(): Boolean = getToken() != null

    override fun clear() {
        delete(KEY_TOKEN)
        delete(KEY_USERNAME)
        delete(KEY_USER_ID)
    }

    // ── Private Keychain helpers ──────────────────────────────────────────────

    @Suppress("UNCHECKED_CAST")
    private fun write(account: String, value: String) {
        delete(account) // SecItemUpdate is awkward; delete-then-add is simpler and reliable
        val data = value.encodeToByteArray().toNSData()
        val query = NSMutableDictionary()
        query.setObject(kSecClassGenericPassword as Any, kSecClass as NSCopying)
        query.setObject(service, kSecAttrService as NSCopying)
        query.setObject(account, kSecAttrAccount as NSCopying)
        query.setObject(data, kSecValueData as NSCopying)
        SecItemAdd(query as CFDictionaryRef, null)
    }

    @Suppress("UNCHECKED_CAST")
    private fun read(account: String): String? {
        val query = NSMutableDictionary()
        query.setObject(kSecClassGenericPassword as Any, kSecClass as NSCopying)
        query.setObject(service, kSecAttrService as NSCopying)
        query.setObject(account, kSecAttrAccount as NSCopying)
        query.setObject(kCFBooleanTrue as Any, kSecReturnData as NSCopying)
        query.setObject(kSecMatchLimitOne as Any, kSecMatchLimit as NSCopying)
        memScoped {
            val resultRef = alloc<CFTypeRefVar>()
            val status = SecItemCopyMatching(query as CFDictionaryRef, resultRef.ptr)
            if (status == errSecSuccess) {
                @Suppress("UNCHECKED_CAST")
                val nsData = CFBridgingRelease(resultRef.value) as? NSData ?: return null
                return nsData.toByteArray().decodeToString()
            }
        }
        return null
    }

    @Suppress("UNCHECKED_CAST")
    private fun delete(account: String) {
        val query = NSMutableDictionary()
        query.setObject(kSecClassGenericPassword as Any, kSecClass as NSCopying)
        query.setObject(service, kSecAttrService as NSCopying)
        query.setObject(account, kSecAttrAccount as NSCopying)
        SecItemDelete(query as CFDictionaryRef)
    }

    // ── ByteArray ↔ NSData ────────────────────────────────────────────────────

    private fun ByteArray.toNSData(): NSData = memScoped {
        NSData.create(bytes = allocArrayOf(this@toNSData), length = size.toULong())
    }

    private fun NSData.toByteArray(): ByteArray {
        val len = length.toInt()
        if (len == 0) return ByteArray(0)
        return ByteArray(len).also { arr ->
            arr.usePinned { pinned ->
                memcpy(pinned.addressOf(0), bytes, len.toULong())
            }
        }
    }

    companion object {
        private const val KEY_TOKEN = "auth_token"
        private const val KEY_USERNAME = "username"
        private const val KEY_USER_ID = "user_id"
    }
}
