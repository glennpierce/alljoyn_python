#!/usr/bin/env python
# -*- coding: utf-8 -*-

import types
import ctypes as C
from ctypes import POINTER
import os, os.path, tempfile, sys, time, StringIO
from warnings import warn
from enum import Enum, unique

#Load the constants
from constants import *
import library

@unique
class QStatus(Enum):
    ER_OK = 0x0 # Success.
    ER_FAIL = 0x1 # Generic failure.
    ER_UTF_CONVERSION_FAILED = 0x2 # Conversion between UTF bases failed.
    ER_BUFFER_TOO_SMALL = 0x3 # Not enough space in buffer for operation.
    ER_OS_ERROR = 0x4 # Underlying OS has indicated an error.
    ER_OUT_OF_MEMORY = 0x5 # Failed to allocate memory.
    ER_SOCKET_BIND_ERROR = 0x6 # Bind to IP address failed.
    ER_INIT_FAILED = 0x7 # Initialization failed.
    ER_WOULDBLOCK = 0x8 # An I/O attempt on non-blocking resource would block
    ER_NOT_IMPLEMENTED = 0x9 # Feature not implemented
    ER_TIMEOUT = 0xa # Operation timed out
    ER_SOCK_OTHER_END_CLOSED = 0xb # Other end closed the socket
    ER_BAD_ARG_1 = 0xc # Function call argument 1 is invalid
    ER_BAD_ARG_2 = 0xd # Function call argument 2 is invalid
    ER_BAD_ARG_3 = 0xe # Function call argument 3 is invalid
    ER_BAD_ARG_4 = 0xf # Function call argument 4 is invalid
    ER_BAD_ARG_5 = 0x10 # Function call argument 5 is invalid
    ER_BAD_ARG_6 = 0x11 # Function call argument 6 is invalid
    ER_BAD_ARG_7 = 0x12 # Function call argument 7 is invalid
    ER_BAD_ARG_8 = 0x13 # Function call argument 8 is invalid
    ER_INVALID_ADDRESS = 0x14 # Address is NULL or invalid
    ER_INVALID_DATA = 0x15 # Generic invalid data error
    ER_READ_ERROR = 0x16 # Generic read error
    ER_WRITE_ERROR = 0x17 # Generic write error
    ER_OPEN_FAILED = 0x18 # Generic open failure
    ER_PARSE_ERROR = 0x19 # Generic parse failure
    ER_END_OF_DATA = 0x1A # Generic EOD/EOF error
    ER_CONN_REFUSED = 0x1B # Connection was refused because no one is listening
    ER_BAD_ARG_COUNT = 0x1C # Incorrect number of arguments given to function call
    ER_WARNING = 0x1D # Generic warning
    ER_EOF = 0x1E # End of file
    ER_DEADLOCK = 0x1F # Operation would cause deadlock
    ER_COMMON_ERRORS = 0x1000 # Error code block for the Common subsystem.
    ER_STOPPING_THREAD = 0x1001 # Operation interrupted by ERThread stop signal.
    ER_ALERTED_THREAD = 0x1002 # Operation interrupted by ERThread alert signal.
    ER_XML_MALFORMED = 0x1003 # Cannot parse malformed XML
    ER_AUTH_FAIL = 0x1004 # Authentication failed
    ER_AUTH_USER_REJECT = 0x1005 # Authentication was rejected by user
    ER_NO_SUCH_ALARM = 0x1006 # Attempt to reference non-existent timer alarm
    ER_TIMER_FALLBEHIND = 0x1007 # A timer thread is missing scheduled alarm times
    ER_SSL_ERRORS = 0x1008 # Error code block for SSL subsystem
    ER_SSL_INIT = 0x1009 # SSL initialization failed.
    ER_SSL_CONNECT = 0x100a # Failed to connect to remote host using SSL
    ER_SSL_VERIFY = 0x100b # Failed to verify identity of SSL destination
    ER_EXTERNAL_THREAD = 0x100c # Operation not supported on external thread wrapper
    ER_CRYPTO_ERROR = 0x100d # Non-specific error in the crypto subsystem
    ER_CRYPTO_TRUNCATED = 0x100e # Not enough room for key
    ER_CRYPTO_KEY_UNAVAILABLE = 0x100f # No key to return
    ER_BAD_HOSTNAME = 0x1010 # Cannot lookup hostname
    ER_CRYPTO_KEY_UNUSABLE = 0x1011 # Key cannot be used
    ER_EMPTY_KEY_BLOB = 0x1012 # Key blob is empty
    ER_CORRUPT_KEYBLOB = 0x1013 # Key blob is corrupted
    ER_INVALID_KEY_ENCODING = 0x1014 # Encoded key is not valid
    ER_DEAD_THREAD = 0x1015 # Operation not allowed thread is dead
    ER_THREAD_RUNNING = 0x1016 # Cannot start a thread that is already running
    ER_THREAD_STOPPING = 0x1017 # Cannot start a thread that is already stopping
    ER_BAD_STRING_ENCODING = 0x1018 # Encoded string did not have the expected format or contents
    ER_CRYPTO_INSUFFICIENT_SECURITY = 0x1019 # Crypto algorithm parameters do not provide sufficient security
    ER_CRYPTO_ILLEGAL_PARAMETERS = 0x101a # Crypto algorithm parameter value is illegal
    ER_CRYPTO_HASH_UNINITIALIZED = 0x101b # Cryptographic hash function must be initialized
    ER_THREAD_NO_WAIT = 0x101c # Thread cannot be blocked by a WAIT or SLEEP call
    ER_TIMER_EXITING = 0x101d # Cannot add an alarm to a timer that is exiting
    ER_INVALID_GUID = 0x101e # String is not a hex encoded GUID string
    ER_THREADPOOL_EXHAUSTED = 0x101f # A thread pool has reached its specified concurrency
    ER_THREADPOOL_STOPPING = 0x1020 # Cannot execute a closure on a stopping thread pool
    ER_INVALID_STREAM = 0x1021 # Attempt to reference non-existent stream entry
    ER_TIMER_FULL = 0x1022 # Attempt to reference non-existent stream entry
    ER_IODISPATCH_STOPPING = 0x1023 # Cannot execute a read or write command on an IODispatch thread because it is stopping.
    ER_SLAP_INVALID_PACKET_LEN = 0x1024 # Length of SLAP packet is invalid.
    ER_SLAP_HDR_CHECKSUM_ERROR = 0x1025 # SLAP packet header checksum error.
    ER_SLAP_INVALID_PACKET_TYPE = 0x1026 # Invalid SLAP packet type.
    ER_SLAP_LEN_MISMATCH = 0x1027 # Calculated length does not match the received length.
    ER_SLAP_PACKET_TYPE_MISMATCH = 0x1028 # Packet type does not match reliability bit.
    ER_SLAP_CRC_ERROR = 0x1029 # SLAP packet CRC error.
    ER_SLAP_ERROR = 0x102A # Generic SLAP error.
    ER_SLAP_OTHER_END_CLOSED = 0x102B # Other end closed the SLAP connection
    ER_TIMER_NOT_ALLOWED = 0x102C # Timer EnableReentrancy call not allowed
    ER_NONE = 0xffff # No error code to report
    ER_BUS_ERRORS = 0x9000 # Error code block for ALLJOYN wire protocol
    ER_BUS_READ_ERROR = 0x9001 # Error attempting to read
    ER_BUS_WRITE_ERROR = 0x9002 # Error attempting to write
    ER_BUS_BAD_VALUE_TYPE = 0x9003 # Read an invalid value type
    ER_BUS_BAD_HEADER_FIELD = 0x9004 # Read an invalid header field
    ER_BUS_BAD_SIGNATURE = 0x9005 # Signature was badly formed
    ER_BUS_BAD_OBJ_PATH = 0x9006 # Object path contained an illegal character
    ER_BUS_BAD_MEMBER_NAME = 0x9007 # A member name contained an illegal character
    ER_BUS_BAD_INTERFACE_NAME = 0x9008 # An interface name contained an illegal character
    ER_BUS_BAD_ERROR_NAME = 0x9009 # An error name contained an illegal character
    ER_BUS_BAD_BUS_NAME = 0x900a # A bus name contained an illegal character
    ER_BUS_NAME_TOO_LONG = 0x900b # A name exceeded the permitted length
    ER_BUS_BAD_LENGTH = 0x900c # Length of an array was not a multiple of the array element size
    ER_BUS_BAD_VALUE = 0x900d # Parsed value in a message was invalid (for example: boolean > 1) 
    ER_BUS_BAD_HDR_FLAGS = 0x900e # Unknown header flags
    ER_BUS_BAD_BODY_LEN = 0x900f # Body length was to long or too short
    ER_BUS_BAD_HEADER_LEN = 0x9010 # Header length was to long or too short
    ER_BUS_UNKNOWN_SERIAL = 0x9011 # Serial number in a method response was unknown
    ER_BUS_UNKNOWN_PATH = 0x9012 # Path in a method call or signal was unknown
    ER_BUS_UNKNOWN_INTERFACE = 0x9013 # Interface in a method call or signal was unknown
    ER_BUS_ESTABLISH_FAILED = 0x9014 # Failed to establish a connection
    ER_BUS_UNEXPECTED_SIGNATURE = 0x9015 # Signature in message was not what was expected
    ER_BUS_INTERFACE_MISSING = 0x9016 # Interface header field is missing
    ER_BUS_PATH_MISSING = 0x9017 # Object path header field is missing
    ER_BUS_MEMBER_MISSING = 0x9018 # Member header field is missing
    ER_BUS_REPLY_SERIAL_MISSING = 0x9019 # Reply-Serial header field is missing
    ER_BUS_ERROR_NAME_MISSING = 0x901a # Error Name header field is missing
    ER_BUS_INTERFACE_NO_SUCH_MEMBER = 0x901b # Interface does not have the requested member
    ER_BUS_NO_SUCH_OBJECT = 0x901c # Object does not exist
    ER_BUS_OBJECT_NO_SUCH_MEMBER = 0x901d # Object does not have the requested member (on any interface)
    ER_BUS_OBJECT_NO_SUCH_INTERFACE = 0x901e # Object does not have the requested interface
    ER_BUS_NO_SUCH_INTERFACE = 0x901f # Requested interface does not exist
    ER_BUS_MEMBER_NO_SUCH_SIGNATURE = 0x9020 # Member exists but does not have the requested signature
    ER_BUS_NOT_NUL_TERMINATED = 0x9021 # A string or signature was not NUL terminated
    ER_BUS_NO_SUCH_PROPERTY = 0x9022 # No such property for a GET or SET operation 
    ER_BUS_SET_WRONG_SIGNATURE = 0x9023 # Attempt to set a property value with the wrong signature
    ER_BUS_PROPERTY_VALUE_NOT_SET = 0x9024 # Attempt to get a property whose value has not been set
    ER_BUS_PROPERTY_ACCESS_DENIED = 0x9025 # Attempt to set or get a property failed due to access rights
    ER_BUS_NO_TRANSPORTS = 0x9026 # No physical message transports were specified
    ER_BUS_BAD_TRANSPORT_ARGS = 0x9027 # Missing or badly formatted transports args specified
    ER_BUS_NO_ROUTE = 0x9028 # Message cannot be routed to destination
    ER_BUS_NO_ENDPOINT = 0x9029 # An endpoint with given name cannot be found
    ER_BUS_BAD_SEND_PARAMETER = 0x902a # Bad parameter in send message call
    ER_BUS_UNMATCHED_REPLY_SERIAL = 0x902b # Serial number in method call reply message did not match any method calls
    ER_BUS_BAD_SENDER_ID = 0x902c # Sender identifier is invalid
    ER_BUS_TRANSPORT_NOT_STARTED = 0x902d # Attempt to send on a transport that has not been started
    ER_BUS_EMPTY_MESSAGE = 0x902e # Attempt to deliver an empty message
    ER_BUS_NOT_OWNER = 0x902f # A bus name operation was not permitted because sender does not own name
    ER_BUS_SET_PROPERTY_REJECTED = 0x9030 # Application rejected a request to set a property
    ER_BUS_CONNECT_FAILED = 0x9031 # Connection failed
    ER_BUS_REPLY_IS_ERROR_MESSAGE = 0x9032 # Response from a method call was an ERROR message
    ER_BUS_NOT_AUTHENTICATING = 0x9033 # Not in an authentication conversation
    ER_BUS_NO_LISTENER = 0x9034 # A listener is required to implement the requested function
    ER_BUS_NOT_ALLOWED = 0x9036 # The operation attempted is not allowed
    ER_BUS_WRITE_QUEUE_FULL = 0x9037 # Write failed because write queue is full
    ER_BUS_ENDPOINT_CLOSING = 0x9038 # Operation not permitted on endpoint in process of closing
    ER_BUS_INTERFACE_MISMATCH = 0x9039 # Received two conflicting definitions for the same interface
    ER_BUS_MEMBER_ALREADY_EXISTS = 0x903a # Attempt to add a member to an interface that already exists
    ER_BUS_PROPERTY_ALREADY_EXISTS = 0x903b # Attempt to add a property to an interface that already exists
    ER_BUS_IFACE_ALREADY_EXISTS = 0x903c # Attempt to add an interface to an object that already exists
    ER_BUS_ERROR_RESPONSE = 0x903d # Received an error response to a method call
    ER_BUS_BAD_XML = 0x903e # XML data is improperly formatted
    ER_BUS_BAD_CHILD_PATH = 0x903f # The path of a child object is incorrect given its parent's path
    ER_BUS_OBJ_ALREADY_EXISTS = 0x9040 # Attempt to add a RemoteObject child that already exists
    ER_BUS_OBJ_NOT_FOUND = 0x9041 # Object with given path does not exist
    ER_BUS_CANNOT_EXPAND_MESSAGE = 0x9042 # Expansion information for a compressed message is not available
    ER_BUS_NOT_COMPRESSED = 0x9043 # Attempt to expand a message that is not compressed
    ER_BUS_ALREADY_CONNECTED = 0x9044 # Attempt to connect to a bus which is already connected
    ER_BUS_NOT_CONNECTED = 0x9045 # Attempt to use a bus attachment that is not connected to a router
    ER_BUS_ALREADY_LISTENING = 0x9046 # Attempt to listen on a bus address which is already being listened on
    ER_BUS_KEY_UNAVAILABLE = 0x9047 # The request key is not available
    ER_BUS_TRUNCATED = 0x9048 # Insufficient memory to copy data
    ER_BUS_KEY_STORE_NOT_LOADED = 0x9049 # Accessing the key store before it is loaded
    ER_BUS_NO_AUTHENTICATION_MECHANISM = 0x904a # There is no authentication mechanism
    ER_BUS_BUS_ALREADY_STARTED = 0x904b # Bus has already been started
    ER_BUS_BUS_NOT_STARTED = 0x904c # Bus has not yet been started
    ER_BUS_KEYBLOB_OP_INVALID = 0x904d # The operation requested cannot be performed using this key blob
    ER_BUS_INVALID_HEADER_CHECKSUM = 0x904e # Invalid header checksum in an encrypted message
    ER_BUS_MESSAGE_NOT_ENCRYPTED = 0x904f # Security policy requires the message to be encrypted
    ER_BUS_INVALID_HEADER_SERIAL = 0x9050 # Serial number in message header is invalid
    ER_BUS_TIME_TO_LIVE_EXPIRED = 0x9051 # Message time-to-live has expired
    ER_BUS_HDR_EXPANSION_INVALID = 0x9052 # Something is wrong with a header expansion
    ER_BUS_MISSING_COMPRESSION_TOKEN = 0x9053 # Compressed headers require a compression token
    ER_BUS_NO_PEER_GUID = 0x9054 # There is no GUID for this peer
    ER_BUS_MESSAGE_DECRYPTION_FAILED = 0x9055 # Message decryption failed
    ER_BUS_SECURITY_FATAL = 0x9056 # A fatal security failure
    ER_BUS_KEY_EXPIRED = 0x9057 # An encryption key has expired
    ER_BUS_CORRUPT_KEYSTORE = 0x9058 # Key store is corrupt
    ER_BUS_NO_CALL_FOR_REPLY = 0x9059 # A reply only allowed in response to a method call
    ER_BUS_NOT_A_COMPLETE_TYPE = 0x905a # Signature must be a single complete type
    ER_BUS_POLICY_VIOLATION = 0x905b # Message does not meet policy restrictions
    ER_BUS_NO_SUCH_SERVICE = 0x905c # Service name is unknown
    ER_BUS_TRANSPORT_NOT_AVAILABLE = 0x905d # Transport cannot be used due to underlying mechanism disabled by OS
    ER_BUS_INVALID_AUTH_MECHANISM = 0x905e # Authentication mechanism is not valid
    ER_BUS_KEYSTORE_VERSION_MISMATCH = 0x905f # Key store has wrong version number
    ER_BUS_BLOCKING_CALL_NOT_ALLOWED = 0x9060 # A synchronous method call from within handler is not permitted.
    ER_BUS_SIGNATURE_MISMATCH = 0x9061 # MsgArg(s) do not match signature.
    ER_BUS_STOPPING = 0x9062 # The bus is stopping.
    ER_BUS_METHOD_CALL_ABORTED = 0x9063 # The method call was aborted.
    ER_BUS_CANNOT_ADD_INTERFACE = 0x9064 # An interface cannot be added to an object that is already registered.
    ER_BUS_CANNOT_ADD_HANDLER = 0x9065 # A method handler cannot be added to an object that is already registered.
    ER_BUS_KEYSTORE_NOT_LOADED = 0x9066 # Key store has not been loaded
    ER_BUS_NO_SUCH_HANDLE = 0x906b # Handle is not in the handle table
    ER_BUS_HANDLES_NOT_ENABLED = 0x906c # Passing of handles is not enabled for this connection
    ER_BUS_HANDLES_MISMATCH = 0x906d # Message had more handles than expected
    ER_BUS_NO_SESSION = 0x906f # Session id is not valid
    ER_BUS_ELEMENT_NOT_FOUND = 0x9070 # Dictionary element was not found
    ER_BUS_NOT_A_DICTIONARY = 0x9071 # MsgArg was not an array of dictionary elements
    ER_BUS_WAIT_FAILED = 0x9072 # Wait failed
    ER_BUS_BAD_SESSION_OPTS = 0x9074 # Session options are bad or incompatible
    ER_BUS_CONNECTION_REJECTED = 0x9075 # Incoming connection rejected
    ER_DBUS_REQUEST_NAME_REPLY_PRIMARY_OWNER = 0x9076 # RequestName reply: Name was successfully obtained
    ER_DBUS_REQUEST_NAME_REPLY_IN_QUEUE = 0x9077 # RequestName reply: Name is already owned, request for name has been queued
    ER_DBUS_REQUEST_NAME_REPLY_EXISTS = 0x9078 # RequestName reply: Name is already owned and DO_NOT_QUEUE was specified in request
    ER_DBUS_REQUEST_NAME_REPLY_ALREADY_OWNER = 0x9079 # RequestName reply: Name is already owned by this endpoint
    ER_DBUS_RELEASE_NAME_REPLY_RELEASED = 0x907a # ReleaseName reply: Name was released
    ER_DBUS_RELEASE_NAME_REPLY_NON_EXISTENT = 0x907b #  ReleaseName reply: Name does not exist
    ER_DBUS_RELEASE_NAME_REPLY_NOT_OWNER = 0x907c # ReleaseName reply: Request to release name that is not owned by this endpoint
    ER_DBUS_START_REPLY_ALREADY_RUNNING = 0x907e # StartServiceByName reply: Service is already running
    ER_ALLJOYN_BINDSESSIONPORT_REPLY_ALREADY_EXISTS = 0x9080 # BindSessionPort reply: SessionPort already exists
    ER_ALLJOYN_BINDSESSIONPORT_REPLY_FAILED = 0x9081 # BindSessionPort reply: Failed
    ER_ALLJOYN_JOINSESSION_REPLY_NO_SESSION = 0x9083 # JoinSession reply: Session with given name does not exist
    ER_ALLJOYN_JOINSESSION_REPLY_UNREACHABLE = 0x9084 # JoinSession reply: Failed to find suitable transport
    ER_ALLJOYN_JOINSESSION_REPLY_CONNECT_FAILED = 0x9085 # JoinSession reply: Connect to advertised address
    ER_ALLJOYN_JOINSESSION_REPLY_REJECTED = 0x9086 # JoinSession reply: The session creator rejected the join req
    ER_ALLJOYN_JOINSESSION_REPLY_BAD_SESSION_OPTS = 0x9087 # JoinSession reply: Failed due to session option incompatibilities
    ER_ALLJOYN_JOINSESSION_REPLY_FAILED = 0x9088 # JoinSession reply: Failed for unknown reason
    ER_ALLJOYN_LEAVESESSION_REPLY_NO_SESSION = 0x908a # LeaveSession reply: Session with given name does not exist
    ER_ALLJOYN_LEAVESESSION_REPLY_FAILED = 0x908b # LeaveSession reply: Failed for unspecified reason
    ER_ALLJOYN_ADVERTISENAME_REPLY_TRANSPORT_NOT_AVAILABLE = 0x908c # AdvertiseName reply: The specified transport is unavailable for advertising
    ER_ALLJOYN_ADVERTISENAME_REPLY_ALREADY_ADVERTISING = 0x908d # AdvertiseName reply: This endpoint is already advertising this name
    ER_ALLJOYN_ADVERTISENAME_REPLY_FAILED = 0x908e # AdvertiseName reply: Advertise failed
    ER_ALLJOYN_CANCELADVERTISENAME_REPLY_FAILED = 0x9090 # CancelAdvertiseName reply: Advertise failed
    ER_ALLJOYN_FINDADVERTISEDNAME_REPLY_TRANSPORT_NOT_AVAILABLE = 0x9091 # FindAdvertisedName reply: The specified transport is unavailable for discovery
    ER_ALLJOYN_FINDADVERTISEDNAME_REPLY_ALREADY_DISCOVERING = 0x9092 # FindAdvertisedName reply: This endpoint is already discovering this name
    ER_ALLJOYN_FINDADVERTISEDNAME_REPLY_FAILED = 0x9093 # FindAdvertisedName reply: Failed
    ER_ALLJOYN_CANCELFINDADVERTISEDNAME_REPLY_FAILED = 0x9095 # CancelFindAdvertisedName reply: Failed
    ER_BUS_UNEXPECTED_DISPOSITION = 0x9096 # An unexpected disposition was returned and has been treated as an error
    ER_BUS_INTERFACE_ACTIVATED = 0x9097 # An InterfaceDescription cannot be modified once activated
    ER_ALLJOYN_UNBINDSESSIONPORT_REPLY_BAD_PORT = 0x9098 # UnbindSessionPort reply: SessionPort does not exist
    ER_ALLJOYN_UNBINDSESSIONPORT_REPLY_FAILED = 0x9099 # UnbindSessionPort reply: Failed
    ER_ALLJOYN_BINDSESSIONPORT_REPLY_INVALID_OPTS = 0x909a # BindSessionPort reply: SessionOpts are invalid
    ER_ALLJOYN_JOINSESSION_REPLY_ALREADY_JOINED = 0x909b # JoinSession reply: Caller has already joined the session
    ER_BUS_SELF_CONNECT = 0x909c # Received BusHello from self
    ER_BUS_SECURITY_NOT_ENABLED = 0x909d # Security is not enabled for this bus attachment
    ER_BUS_LISTENER_ALREADY_SET = 0x909e # A listener has already been set
    ER_BUS_PEER_AUTH_VERSION_MISMATCH = 0x909f # Incompatible peer authentication version numbers
    ER_ALLJOYN_SETLINKTIMEOUT_REPLY_NOT_SUPPORTED = 0x90a0 # Local router does not support SetLinkTimeout
    ER_ALLJOYN_SETLINKTIMEOUT_REPLY_NO_DEST_SUPPORT = 0x90a1 # SetLinkTimeout not supported by destination
    ER_ALLJOYN_SETLINKTIMEOUT_REPLY_FAILED = 0x90a2 # SetLinkTimeout failed
    ER_ALLJOYN_ACCESS_PERMISSION_WARNING = 0x90a3 # No permission to use Wifi
    ER_ALLJOYN_ACCESS_PERMISSION_ERROR = 0x90a4 # No permission to access peer service
    ER_BUS_DESTINATION_NOT_AUTHENTICATED = 0x90a5 # Cannot send a signal to a destination that is not authenticated
    ER_BUS_ENDPOINT_REDIRECTED = 0x90a6 # Endpoint was redirected to another address
    ER_BUS_AUTHENTICATION_PENDING = 0x90a7 # Authentication of remote peer is pending
    ER_BUS_NOT_AUTHORIZED = 0x90a8 # Operation was not authorized
    ER_PACKET_BUS_NO_SUCH_CHANNEL = 0x90a9 # Received packet for unknown channel
    ER_PACKET_BAD_FORMAT = 0x90aa # Received packet with incorrect header information
    ER_PACKET_CONNECT_TIMEOUT = 0x90ab # Timed out waiting for connect response
    ER_PACKET_CHANNEL_FAIL = 0x90ac # Failed to create new comm channel
    ER_PACKET_TOO_LARGE = 0x90ad # Message too large for use with packet based transport
    ER_PACKET_BAD_PARAMETER = 0x90ae # Invalid PacketEngine control packet received
    ER_PACKET_BAD_CRC = 0x90af # Packet has invalid CRC
    ER_RENDEZVOUS_SERVER_DEACTIVATED_USER = 0x90cb # Rendezvous Server has deactivated the current user. Register with the Rendezvous Server to continue.
    ER_RENDEZVOUS_SERVER_UNKNOWN_USER = 0x90cc # Rendezvous Server does not recognize the current user. Register with the Rendezvous Server to continue.
    ER_UNABLE_TO_CONNECT_TO_RENDEZVOUS_SERVER = 0x90cd # Unable to connect to the Rendezvous Server
    ER_NOT_CONNECTED_TO_RENDEZVOUS_SERVER = 0x90ce # Not connected to the Rendezvous Server
    ER_UNABLE_TO_SEND_MESSAGE_TO_RENDEZVOUS_SERVER = 0x90cf # Unable to send message to the Rendezvous Server
    ER_INVALID_RENDEZVOUS_SERVER_INTERFACE_MESSAGE = 0x90d0 # Invalid Rendezvous Server interface message
    ER_INVALID_PERSISTENT_CONNECTION_MESSAGE_RESPONSE = 0x90d1 # Invalid message response received over the Persistent connection with the Rendezvous Server
    ER_INVALID_ON_DEMAND_CONNECTION_MESSAGE_RESPONSE = 0x90d2 # Invalid message response received over the On Demand connection with the Rendezvous Server
    ER_INVALID_HTTP_METHOD_USED_FOR_RENDEZVOUS_SERVER_INTERFACE_MESSAGE = 0x90d3 # Invalid HTTP method type used for Rendezvous Server interface message
    ER_RENDEZVOUS_SERVER_ERR500_INTERNAL_ERROR = 0x90d4 # Received a HTTP 500 status code from the Rendezvous Server. This indicates an internal error in the Server
    ER_RENDEZVOUS_SERVER_ERR503_STATUS_UNAVAILABLE = 0x90d5 # Received a HTTP 503 status code from the Rendezvous Server. This indicates unavailability of the Server error state
    ER_RENDEZVOUS_SERVER_ERR401_UNAUTHORIZED_REQUEST = 0x90d6 # Received a HTTP 401 status code from the Rendezvous Server. This indicates that the client is unauthorized to send a request to the Server. The Client login procedure must be initiated.
    ER_RENDEZVOUS_SERVER_UNRECOVERABLE_ERROR = 0x90d7 # Received a HTTP status code indicating unrecoverable error from the Rendezvous Server. The connection with the Server should be re-established.
    ER_RENDEZVOUS_SERVER_ROOT_CERTIFICATE_UNINITIALIZED = 0x90d8 # Rendezvous Server root ceritificate uninitialized.
    ER_BUS_NO_SUCH_ANNOTATION = 0x90d9 # No such annotation for a GET or SET operation 
    ER_BUS_ANNOTATION_ALREADY_EXISTS = 0x90da # Attempt to add an annotation to an interface or property that already exists
    ER_SOCK_CLOSING = 0x90db # Socket close in progress
    ER_NO_SUCH_DEVICE = 0x90dc # A referenced device cannot be located
    ER_P2P = 0x90dd # An error occurred in a Wi-Fi Direct helper method call
    ER_P2P_TIMEOUT = 0x90de # A timeout occurred in a Wi-Fi Direct helper method call
    ER_P2P_NOT_CONNECTED = 0x90df # A required Wi-Fi Direct network connection does not exist
    ER_BAD_TRANSPORT_MASK = 0x90e0 # Exactly one mask bit was not set in the provided TransportMask
    ER_PROXIMITY_CONNECTION_ESTABLISH_FAIL = 0x90e1 # Fail to establish P2P proximity connection
    ER_PROXIMITY_NO_PEERS_FOUND = 0x90e2 # Cannot find proximity P2P peers
    ER_BUS_OBJECT_NOT_REGISTERED = 0x90e3 # Operation not permitted on unregistered bus object
    ER_P2P_DISABLED = 0x90e4 # Wi-Fi Direct is disabled on the device
    ER_P2P_BUSY = 0x90e5 # Wi-Fi Direct resources are in busy state
    ER_BUS_INCOMPATIBLE_DAEMON = 0x90e6 # The router version is too old to be used by this client
    ER_P2P_NO_GO = 0x90e7 # Attempt to execute a Wi-Fi Direct GO-related operation while STA
    ER_P2P_NO_STA = 0x90e8 # Attempt to execute a Wi-Fi Direct STA-related operation while GO
    ER_P2P_FORBIDDEN = 0x90e9 # Attempt to execute a forbidden Wi-Fi Direct operation
    ER_ALLJOYN_ONAPPSUSPEND_REPLY_FAILED = 0x90ea # OnAppSuspend reply: Failed
    ER_ALLJOYN_ONAPPSUSPEND_REPLY_UNSUPPORTED = 0x90eb # OnAppSuspend reply: Unsupported operation
    ER_ALLJOYN_ONAPPRESUME_REPLY_FAILED = 0x90ec # OnAppResume reply: Failed
    ER_ALLJOYN_ONAPPRESUME_REPLY_UNSUPPORTED = 0x90ed # OnAppResume reply: Unsupported operation
    ER_BUS_NO_SUCH_MESSAGE = 0x90ee # Message not found
    ER_ALLJOYN_REMOVESESSIONMEMBER_REPLY_NO_SESSION = 0x90ef # RemoveSessionMember reply: Specified session Id with this endpoint was not found
    ER_ALLJOYN_REMOVESESSIONMEMBER_NOT_BINDER = 0x90f0 # RemoveSessionMember reply: Endpoint is not the binder of session
    ER_ALLJOYN_REMOVESESSIONMEMBER_NOT_MULTIPOINT = 0x90f1 # RemoveSessionMember reply: Session is not multipoint
    ER_ALLJOYN_REMOVESESSIONMEMBER_NOT_FOUND = 0x90f2 # RemoveSessionMember reply: Specified session member was not found
    ER_ALLJOYN_REMOVESESSIONMEMBER_INCOMPATIBLE_REMOTE_DAEMON = 0x90f3 # RemoveSessionMember reply: The remote router does not support this feature
    ER_ALLJOYN_REMOVESESSIONMEMBER_REPLY_FAILED = 0x90f4 # RemoveSessionMember reply: Failed for unspecified reason
    ER_BUS_REMOVED_BY_BINDER = 0x90f5 # The session member was removed by the binder
    ER_BUS_MATCH_RULE_NOT_FOUND = 0x90f6 # The match rule was not found
    ER_ALLJOYN_PING_FAILED = 0x90f7 # Ping failed
    ER_ALLJOYN_PING_REPLY_UNREACHABLE = 0x90f8 # Name pinged is unreachable
    ER_UDP_MSG_TOO_LONG = 0x90f9 # The message is too long to transmit over the UDP transport
    ER_UDP_DEMUX_NO_ENDPOINT = 0x90fa # Tried to demux the callback but found no endpoint for the connection
    ER_UDP_NO_NETWORK = 0x90fb # Not listening on network implied by IP address
    ER_UDP_UNEXPECTED_LENGTH = 0x90fc # Request for more bytes than are in the underlying datagram
    ER_UDP_UNEXPECTED_FLOW = 0x90fd # The data flow type of the endpoint has an unexpected value
    ER_UDP_DISCONNECT = 0x90fe # Unexpected disconnect occurred
    ER_UDP_NOT_IMPLEMENTED = 0x90ff # Feature not implemented for the UDP transport
    ER_UDP_NO_LISTENER = 0x9100 # Discovery started with no listener to receive callbacks
    ER_UDP_STOPPING = 0x9101 # Attempt to use UDP when transport stopping
    ER_ARDP_BACKPRESSURE = 0x9102 # ARDP is applying backpressure -- send window is full
    ER_UDP_BACKPRESSURE = 0x9103 # UDP is applying backpressure to ARDP -- queue is full
    ER_ARDP_INVALID_STATE = 0x9104 # Current ARDP state does not allow attempted operation
    ER_ARDP_TTL_EXPIRED = 0x9105 # Time-To-Live of ARDP segment has expired
    ER_ARDP_PERSIST_TIMEOUT = 0x9106 # Remote endpoint stopped consuming data -- send window is full
    ER_ARDP_PROBE_TIMEOUT = 0x9107 # ARDP link timeout
    ER_ARDP_REMOTE_CONNECTION_RESET = 0x9108 # Remote endpoint disconected: sent RST
    ER_UDP_BUSHELLO = 0x9109 # UDP Transport is unable to complete an operation relating to a BusHello Message
    ER_UDP_MESSAGE = 0x910a # UDP Transport is unable to complete an operation on an AllJoyn Message
    ER_UDP_INVALID = 0x910b # UDP Transport detected invalid data or parameters from network
    ER_UDP_UNSUPPORTED = 0x910c # UDP Transport does not support the indicated operation or type
    ER_UDP_ENDPOINT_STALLED = 0x910d # UDP Transport has detected an endpoint that is not terminating correctly
    ER_ARDP_INVALID_RESPONSE = 0x910e # ARDP Transport detected invalid message data that causes disconnect
    ER_ARDP_INVALID_CONNECTION = 0x910f # ARDP connection not found
    ER_UDP_LOCAL_DISCONNECT = 0x9110 # UDP Transport connection (intentionally) disconnected on local side
    ER_UDP_EARLY_EXIT = 0x9111 # UDP Transport connection aborted during setup
    ER_UDP_LOCAL_DISCONNECT_FAIL = 0x9112 # UDP Transport local connection disconnect failure
    ER_ARDP_DISCONNECTING = 0x9113 # ARDP connection is being shut down
    ER_ALLJOYN_PING_REPLY_INCOMPATIBLE_REMOTE_ROUTING_NODE = 0x9114 # Remote routing node does not implement Ping
    ER_ALLJOYN_PING_REPLY_TIMEOUT = 0x9115 # Ping call timeout
    ER_ALLJOYN_PING_REPLY_UNKNOWN_NAME = 0x9116 # Name not found currently or part of any known session
    ER_ALLJOYN_PING_REPLY_FAILED = 0x9117 # Generic Ping call error
    ER_TCP_MAX_UNTRUSTED = 0x9118 # The maximum configured number of Thin Library connections has been reached
    ER_ALLJOYN_PING_REPLY_IN_PROGRESS = 0x9119 # A ping request for same name is already in progress
    ER_LANGUAGE_NOT_SUPPORTED = 0x911a # The language requested is not supported
    ER_ABOUT_FIELD_ALREADY_SPECIFIED = 0x911b # A field using the same name is already specified.
    ER_UDP_NOT_DISCONNECTED = 0x911c # A UDP stream was found to be connected during teardown
    ER_UDP_ENDPOINT_NOT_STARTED = 0x911d # Attempt to send on a UDP endpoint that is not started
    ER_UDP_ENDPOINT_REMOVED = 0x911e # Attempt to send on a UDP endpoint that has been removed
    ER_ARDP_VERSION_NOT_SUPPORTED = 0x911f # Specified version of ARDP Protocol is not supported
    ER_CONNECTION_LIMIT_EXCEEDED = 0x9120 # Connection rejected due to configured connection limits
    ER_ARDP_WRITE_BLOCKED = 0x9121 # ARDP cannot write to UDP socket (queue is full)
    ER_PERMISSION_DENIED = 0x9122 # Permission denied
    ER_ABOUT_DEFAULT_LANGUAGE_NOT_SPECIFIED = 0x9123 # Default language must be specified before setting a localized field
    ER_ABOUT_SESSIONPORT_NOT_BOUND = 0x9124 # Unable to announce session port that is not bound to the BusAttachment
    ER_ABOUT_ABOUTDATA_MISSING_REQUIRED_FIELD = 0x9125 # The AboutData is missing a required field.
    ER_ABOUT_INVALID_ABOUTDATA_LISTENER = 0x9126 # The AboutDataListener returns invalid data. Most likely cause: the announced data does not match with non-announced data.
    ER_BUS_PING_GROUP_NOT_FOUND = 0x9127 # Ping group did not exist
    ER_BUS_REMOVED_BY_BINDER_SELF = 0x9128 # The self-joined session member was removed by the binder
    ER_INVALID_CONFIG = 0x9129 # Invalid configuration item or combination of items detected
    ER_ABOUT_INVALID_ABOUTDATA_FIELD_VALUE = 0x912a # General error indicating the value given for an About Data field is invalid.
    ER_ABOUT_INVALID_ABOUTDATA_FIELD_APPID_SIZE = 0x912b # Error indicating the AppId field is not a 128-bit bite array.
    ER_BUS_TRANSPORT_ACCESS_DENIED = 0x912c # The transport denied the connection attempt because the application doesn't have the required permissions.
    ER_INVALID_CERTIFICATE = 0x912d # Invalid certificate
    ER_CERTIFICATE_NOT_FOUND = 0x912e # Certificate not found
    ER_DUPLICATE_CERTIFICATE = 0x912f # Duplicate Certificate found
    ER_UNKNOWN_CERTIFICATE = 0x9130 # Unknown Certificate
    ER_MISSING_DIGEST_IN_CERTIFICATE = 0x9131 # Missing digest in certificate
    ER_DIGEST_MISMATCH = 0x9132 # Digest mismatch
    ER_DUPLICATE_KEY = 0x9133 # Duplicate key found
    ER_NO_COMMON_TRUST = 0x9134 # No common trust anchor found
    ER_MANIFEST_NOT_FOUND = 0x9135 # Permission manifest not found
    ER_INVALID_CERT_CHAIN = 0x9136 # Invalid certificate chain
    ER_NO_TRUST_ANCHOR = 0x9137 # No trust anchor
    ER_INVALID_APPLICATION_STATE = 0x9138 # Invalid application state
    ER_FEATURE_NOT_AVAILABLE = 0x9139 # Feature is not available
    ER_KEY_STORE_ALREADY_INITIALIZED = 0x913a # Key store is already initialized
    ER_KEY_STORE_ID_NOT_YET_SET = 0x913b # Key store ID is not yet set
    ER_POLICY_NOT_NEWER = 0x913c # Installing permission policy not newer than existing policy
    ER_MANIFEST_REJECTED = 0x913d # The manifest of the application was rejected.
    ER_INVALID_CERTIFICATE_USAGE = 0x913e # The certificate extended key usage is not Alljoyn specific.
    ER_INVALID_SIGNAL_EMISSION_TYPE = 0x913f # Attempt to send a signal with the wrong type. */


class QStatusException(Exception):
    def __init__(self, qstatus):
        self.QStatus = qstatus

        # Call the base class constructor with the parameters it needs
        super(QStatusException, self).__init__(self.__QccStatustext(self.QStatus))

    # wrapper for QCC_StatusText returns const char *
    def __QccStatustext(self, status):  # QStatus
        self.__lib.QCC_StatusText.restype = C.c_char_p
        self.__lib.QCC_StatusText.argtypes = [C.c_uint32]
        return self.__lib.QCC_StatusText(status) 
        
#@unique
#class AllJoynEnum(Enum):
#    @staticmethod
#    def CTYPE():
#        return "Sd"

@unique
class SessionLostReasonEnum(Enum):
    INVALID = 0x00
    REMOTE_END_LEFT_SESSION = 0x01
    REMOTE_END_CLOSED_ABRUPTLY = 0x02
    REMOVED_BY_BINDER = 0x03
    LINK_TIMEOUT = 0x04
    REASON_OTHER = 0x05



#alljoyn_about_announceflag
@unique
class AboutAnnounceFlagEnum(Enum):
    UNANNOUNCED = 0x00
    ANNOUNCED = 0x01


#alljoyn_interfacedescription_securitypolicy
@unique
class InterfaceDescriptionSecurityPolicyEnum(Enum):
    AJ_IFC_SECURITY_INHERIT = 0x00
    AJ_IFC_SECURITY_REQUIRED = 0x01
    AJ_IFC_SECURITY_OFF = 0x02


#alljoyn_messagetype
@unique
class SessionLostReasonEnum(Enum):
    ALLJOYN_MESSAGE_INVALID     = 0
    ALLJOYN_MESSAGE_METHOD_CALL = 1,     
    ALLJOYN_MESSAGE_METHOD_RET  = 2,
    ALLJOYN_MESSAGE_ERROR       = 3,
    ALLJOYN_MESSAGE_SIGNAL      = 4


#alljoyn_messagetype
@unique
class MessageTypeEnum(Enum):
    ALLJOYN_MESSAGE_INVALID     = 0, #< an invalid message type
    ALLJOYN_MESSAGE_METHOD_CALL = 1, # a method call message type
    ALLJOYN_MESSAGE_METHOD_RET  = 2, #< a method return message type
    ALLJOYN_MESSAGE_ERROR       = 3, #< an error message type
    ALLJOYN_MESSAGE_SIGNAL      = 4  #< a signal message type

#/** Message types */
#typedef enum {
#    ALLJOYN_MESSAGE_INVALID     = 0, ///< an invalid message type
#    ALLJOYN_MESSAGE_METHOD_CALL = 1, ///< a method call message type
#    ALLJOYN_MESSAGE_METHOD_RET  = 2, ///< a method return message type
#    ALLJOYN_MESSAGE_ERROR       = 3, ///< an error message type
#    ALLJOYN_MESSAGE_SIGNAL      = 4  ///< a signal message type
#} alljoyn_messagetype;



#alljoyn_typeid
#@TypeIdEnum
class MessageTypeEnu(Enum):
    ALLJOYN_INVALID          =  0
    ALLJOYN_ARRAY            = ord('a')
    ALLJOYN_BOOLEAN          = ord('b')
    ALLJOYN_DOUBLE           = ord('d')
    ALLJOYN_DICT_ENTRY       = ord('e')
    ALLJOYN_SIGNATURE        = ord('g')
    ALLJOYN_HANDLE           = ord('h')
    ALLJOYN_INT32            = ord('i')
    ALLJOYN_INT16            = ord('n')
    ALLJOYN_OBJECT_PATH      = ord('o')
    ALLJOYN_UINT16           = ord('q')
    ALLJOYN_STRUCT           = ord('r')
    ALLJOYN_STRING           = ord('s')
    ALLJOYN_UINT64           = ord('t')
    ALLJOYN_UINT32           = ord('u')
    ALLJOYN_VARIANT          = ord('v')
    ALLJOYN_INT64            = ord('x')
    ALLJOYN_BYTE             = ord('y')
    ALLJOYN_STRUCT_OPEN      = ord('(')
    ALLJOYN_STRUCT_CLOSE     = ord(')')
    ALLJOYN_DICT_ENTRY_OPEN  = ord('{')
    ALLJOYN_DICT_ENTRY_CLOSE = ord('}')

    ALLJOYN_BOOLEAN_ARRAY    = (ord('b') << 8) | ord('a')
    ALLJOYN_DOUBLE_ARRAY     = (ord('d') << 8) | ord('a')
    ALLJOYN_INT32_ARRAY      = (ord('i') << 8) | ord('a')
    ALLJOYN_INT16_ARRAY      = (ord('n') << 8) | ord('a')
    ALLJOYN_UINT16_ARRAY     = (ord('q') << 8) | ord('a')
    ALLJOYN_UINT64_ARRAY     = (ord('t') << 8) | ord('a')
    ALLJOYN_UINT32_ARRAY     = (ord('u') << 8) | ord('a')
    ALLJOYN_INT64_ARRAY      = (ord('x') << 8) | ord('a')
    ALLJOYN_BYTE_ARRAY       = (ord('y') << 8) | ord('a')
    ALLJOYN_WILDCARD         = ord('*')



class Constants(object):
    
    QCC_TRUE = 1
    QCC_FALSE = 0

    ALLJOYN_SESSION_ID  = C.c_uint32
    ALLJOYN_SESSION_PORT = C.c_uint16;
    ALLJOYN_TRANSPORT_MASK = C.c_uint16;

    ALLJOYN_LITTLE_ENDIAN = 'l';
    LLJOYN_BIG_ENDIAN    = 'B';

    ALLJOYN_MESSAGE_DEFAULT_TIMEOUT       = 25000;

    ALLJOYN_CRED_PASSWORD     = 0x0001; 
    ALLJOYN_CRED_USER_NAME    = 0x0002; 
    ALLJOYN_CRED_CERT_CHAIN   = 0x0004; 
    ALLJOYN_CRED_PRIVATE_KEY  = 0x0008; 
    ALLJOYN_CRED_LOGON_ENTRY  = 0x0010; 
    ALLJOYN_CRED_EXPIRATION   = 0x0020; 

    ALLJOYN_CRED_NEW_PASSWORD = 0x1001; 
    ALLJOYN_CRED_ONE_TIME_PWD = 0x2001; 



    ALLJOYN_PROP_ACCESS_READ  = 1; 
    ALLJOYN_PROP_ACCESS_WRITE = 2; 
    ALLJOYN_PROP_ACCESS_RW    = 3; 

    ALLJOYN_MEMBER_ANNOTATE_NO_REPLY         = 1; 
    ALLJOYN_MEMBER_ANNOTATE_DEPRECATED       = 2; 
    ALLJOYN_MEMBER_ANNOTATE_SESSIONCAST      = 4; 
    ALLJOYN_MEMBER_ANNOTATE_SESSIONLESS      = 8; 
    ALLJOYN_MEMBER_ANNOTATE_UNICAST          = 16; 
    ALLJOYN_MEMBER_ANNOTATE_GLOBAL_BROADCAST = 32; 


    ALLJOYN_MESSAGE_METHOD_CALL = 1
    
    ALLJOYN_MESSAGE_FLAG_NO_REPLY_EXPECTED  = 0x01

    ALLJOYN_MESSAGE_FLAG_AUTO_START         = 0x02

    ALLJOYN_MESSAGE_FLAG_ALLOW_REMOTE_MSG   = 0x04

    ALLJOYN_MESSAGE_FLAG_SESSIONLESS        = 0x10

    ALLJOYN_MESSAGE_FLAG_GLOBAL_BROADCAST   = 0x20

    ALLJOYN_MESSAGE_FLAG_COMPRESSED         = 0x40  # (attempted_use_of_deprecated_definition = 0x40)

    ALLJOYN_MESSAGE_FLAG_ENCRYPTED          = 0x80


    ALLJOYN_TRAFFIC_TYPE_MESSAGES        = 0x01   
    ALLJOYN_TRAFFIC_TYPE_RAW_UNRELIABLE  = 0x02   
    ALLJOYN_TRAFFIC_TYPE_RAW_RELIABLE    = 0x04   


    ALLJOYN_PROXIMITY_ANY       = 0xFF 
    ALLJOYN_PROXIMITY_PHYSICAL  = 0x01 
    ALLJOYN_PROXIMITY_NETWORK   = 0x02 




###### Callback Types ###################

if sys.platform == 'win32':
    CallbackType = C.WINFUNCTYPE
else:
    CallbackType = C.CFUNCTYPE

BusListenerRegisteredFuncType = CallbackType(None, C.c_void_p, C.c_void_p)                 # const void* context, alljoyn_busattachment bus
BusListenerUnRegisteredFuncType = CallbackType(None, C.c_void_p)                             # const void* context
BusListenerFoundAdvertisedNameFuncType = CallbackType(None, C.c_void_p, C.c_void_p, C.c_void_p, C.c_void_p) # const void* context, const char* name, alljoyn_transportmask transport, const char* namePrefix
BusListenerLostAdvertisedNameFuncType = CallbackType(None, C.c_void_p, C.c_void_p, C.c_void_p, C.c_void_p) # const void* context, const char* name, alljoyn_transportmask transport, const char* namePrefix
BusListenerNameOwnerChangedFuncType = CallbackType(None, C.c_void_p, C.c_void_p, C.c_void_p, C.c_void_p) # const void* context, const char* busName, const char* previousOwner, const char* newOwner
BusListenerBusStoppingFuncType = CallbackType(None, C.c_void_p)                                     # const void* context
BusListenerBusDisconnectedFuncType = CallbackType(None, C.c_void_p)                                     # const void* context
BusListenerBusPropertyChangedFuncType = CallbackType(None, C.c_void_p, C.c_void_p, C.c_void_p)             # const void* context, const char* prop_name, alljoyn_msgarg prop_value
     
     
AboutListenerAnnouncedFuncType = CallbackType(None, C.c_char_p, C.c_void_p, C.c_uint16, C.c_uint16, C.c_void_p) # const void* context ,const char* busName ,uint16_t version ,alljoyn_sessionport port ,const alljoyn_msgarg objectDescriptionArg ,const alljoyn_msgarg aboutDataArg

     
#######################################


######  Structures ####################

class BusListenerCallbacks(C.Structure):
    _fields_ = [("BusListenerRegistered",
                    POINTER(BusListenerRegisteredFuncType)),                 # const void* context, alljoyn_busattachment bus
                ("BusListenerUnRegistered",
                    POINTER(BusListenerUnRegisteredFuncType)),                             # const void* context
                ("BusListenerFoundAdvertisedName", 
                    POINTER(BusListenerFoundAdvertisedNameFuncType)), # const void* context, const char* name, alljoyn_transportmask transport, const char* namePrefix
                ("BusListenerLostAdvertisedName", 
                    POINTER(BusListenerLostAdvertisedNameFuncType)), # const void* context, const char* name, alljoyn_transportmask transport, const char* namePrefix
                ("BusListenerNameOwnerChanged", 
                    POINTER(BusListenerNameOwnerChangedFuncType)), # const void* context, const char* busName, const char* previousOwner, const char* newOwner
                ("BusListenerBusStopping", 
                    POINTER(BusListenerBusStoppingFuncType)),                                     # const void* context
                ("BusListenerBusDisconnected", 
                    POINTER(BusListenerBusDisconnectedFuncType)),                                     # const void* context
                ("BusListenerBusPropertyChanged", 
                    POINTER(BusListenerBusPropertyChangedFuncType))             # const void* context, const char* prop_name, alljoyn_msgarg prop_value
               ]
               


class AboutListenerCallback(C.Structure):
    _fields_ = [("AboutListenerAnnounced",
                    POINTER(AboutListenerAnnouncedFuncType))
               ]
               
               



#      DBusStdDefines.h    
#    MessageReceiver.h 
#  ProxyBusObject.h 
# TransportMask.h
#AboutDataListener.h 
# AutoPinger.h    
# Init.h              
#                               Session.h  
#            version.h
#   
#InterfaceDescription.h  
#Observer.h         
#                SessionListener.h
# BusListener.h  
#  KeyStoreListener.h   
#   PasswordManager.h      
#            SessionPortListener.h
#AboutIconProxy.h     AjAPI.h                   BusObject.h      .              PermissionConfigurationListener.h  Status.h




class AllJoynMeta(type):
   def __new__(cls, name, bases, attrs):
      for attr_name, attr_value in attrs.iteritems():
         if isinstance(attr_value, types.FunctionType):
            attrs[attr_name] = cls.QStatusToException(attr_value)

      return super(DecoMeta, cls).__new__(cls, name, bases, attrs)

   @classmethod
   def QStatusToException(cls, func):
      def wrapper(*args, **kwargs):
         result = func(*args, **kwargs)
         if isinstance(result, QStatus):
            if result != QStatus.ER_OK:
                raise QStatusException(result)
         return result
      return wrapper
      



class AboutData(object):
    
    __metaclass__ = AllJoynMeta
    
    def __init__(self, defaultLanguage, arg=None):
        if not arg:
            self.handle = self.AboutdataCreate(defaultLanguage)
        else:
            self.handle = self.AboutdataCreateFull(arg, defaultLanguage)
    
    def __del__(self):
        self.AboutdataDestroy(self.handle)
    
    def GetFields(self, fields, num_fields):
        self.AboutdataGetfields(self.handle, data, fields, num_fields)
    
    # wrapper for alljoyn_aboutdata_create returns alljoyn_aboutdata
    def AboutdataCreate(self, defaultLanguage):  # const char *
        self.__lib.alljoyn_aboutdata_create.restype = C.c_void_p
        self.__lib.alljoyn_aboutdata_create.argtypes = [C.c_char_p]
        return self.__lib.alljoyn_aboutdata_create(defaultLanguage) 


    # wrapper for alljoyn_aboutdata_create_full returns alljoyn_aboutdata
    def AboutdataCreateFull(self, arg, language):  # const alljoyn_msgarg, const char *
        self.__lib.alljoyn_aboutdata_create_full.restype = C.c_void_p
        self.__lib.alljoyn_aboutdata_create_full.argtypes = [C.c_void_p, C.c_char_p]
        return self.__lib.alljoyn_aboutdata_create_full(arg, language) 


    # wrapper for alljoyn_aboutdata_destroy returns void
    def AboutdataDestroy(self, data):  # alljoyn_aboutdata
        self.__lib.alljoyn_aboutdata_destroy.argtypes = [C.c_void_p]
        self.__lib.alljoyn_aboutdata_destroy(data) 


    # wrapper for alljoyn_aboutdata_createfromxml returns QStatus
    def AboutdataCreatefromxml(self, data, aboutDataXml):  # alljoyn_aboutdata, const char *
        self.__lib.alljoyn_aboutdata_createfromxml.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_createfromxml.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_aboutdata_createfromxml(data, aboutDataXml)) 


    # wrapper for alljoyn_aboutdata_isvalid returns bool
    def AboutdataIsvalid(self, data, language):  # alljoyn_aboutdata, const char *
        self.__lib.alljoyn_aboutdata_isvalid.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_isvalid.argtypes = [C.c_void_p, C.c_char_p]
        return self.__lib.alljoyn_aboutdata_isvalid(data, language) 


    # wrapper for alljoyn_aboutdata_createfrommsgarg returns QStatus
    def AboutdataCreatefrommsgarg(self, data, arg, language):  # alljoyn_aboutdata, const alljoyn_msgarg, const char *
        self.__lib.alljoyn_aboutdata_createfrommsgarg.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_createfrommsgarg.argtypes = [C.c_void_p, C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_aboutdata_createfrommsgarg(data, arg, language)) 


    # wrapper for alljoyn_aboutdata_setappid returns QStatus
    def AboutdataSetappid(self, data, appId, num):  # alljoyn_aboutdata, const uint8_t *, const size_t
        self.__lib.alljoyn_aboutdata_setappid.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_setappid.argtypes = [C.c_void_p, POINTER(C.c_uint8_t), C.csize_t]
        return QStatus(self.__lib.alljoyn_aboutdata_setappid(data, appId, num)) 


    # wrapper for alljoyn_aboutdata_setappid_fromstring returns QStatus
    def AboutdataSetappidFromstring(self, data, appId):  # alljoyn_aboutdata, const char *
        self.__lib.alljoyn_aboutdata_setappid_fromstring.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_setappid_fromstring.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_aboutdata_setappid_fromstring(data, appId)) 


    # wrapper for alljoyn_aboutdata_setdefaultlanguage returns QStatus
    def AboutdataSetdefaultlanguage(self, data, defaultLanguage):  # alljoyn_aboutdata, const char *
        self.__lib.alljoyn_aboutdata_setdefaultlanguage.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_setdefaultlanguage.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_aboutdata_setdefaultlanguage(data, defaultLanguage)) 


    # wrapper for alljoyn_aboutdata_getdefaultlanguage returns QStatus
    def AboutdataGetdefaultlanguage(self, data, defaultLanguage):  # alljoyn_aboutdata, char * *
        self.__lib.alljoyn_aboutdata_getdefaultlanguage.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_getdefaultlanguage.argtypes = [C.c_void_p, POINTER(C.c_char_p)]
        return QStatus(self.__lib.alljoyn_aboutdata_getdefaultlanguage(data, defaultLanguage)) 


    # wrapper for alljoyn_aboutdata_setdevicename returns QStatus
    def AboutdataSetdevicename(self, data, deviceName, language):  # alljoyn_aboutdata, const char *, const char *
        self.__lib.alljoyn_aboutdata_setdevicename.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_setdevicename.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_aboutdata_setdevicename(data, deviceName, language)) 


    # wrapper for alljoyn_aboutdata_getdevicename returns QStatus
    def AboutdataGetdevicename(self, data, deviceName, language):  # alljoyn_aboutdata, char * *, const char *
        self.__lib.alljoyn_aboutdata_getdevicename.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_getdevicename.argtypes = [C.c_void_p, POINTER(C.c_char_p), C.c_char_p]
        return QStatus(self.__lib.alljoyn_aboutdata_getdevicename(data, deviceName, language)) 


    # wrapper for alljoyn_aboutdata_setdeviceid returns QStatus
    def AboutdataSetdeviceid(self, data, deviceId):  # alljoyn_aboutdata, const char *
        self.__lib.alljoyn_aboutdata_setdeviceid.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_setdeviceid.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_aboutdata_setdeviceid(data, deviceId)) 


    # wrapper for alljoyn_aboutdata_getdeviceid returns QStatus
    def AboutdataGetdeviceid(self, data, deviceId):  # alljoyn_aboutdata, char * *
        self.__lib.alljoyn_aboutdata_getdeviceid.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_getdeviceid.argtypes = [C.c_void_p, POINTER(C.c_char_p)]
        return QStatus(self.__lib.alljoyn_aboutdata_getdeviceid(data, deviceId)) 


    # wrapper for alljoyn_aboutdata_setappname returns QStatus
    def AboutdataSetappname(self, data, appName, language):  # alljoyn_aboutdata, const char *, const char *
        self.__lib.alljoyn_aboutdata_setappname.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_setappname.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_aboutdata_setappname(data, appName, language)) 


    # wrapper for alljoyn_aboutdata_getappname returns QStatus
    def AboutdataGetappname(self, data, appName, language):  # alljoyn_aboutdata, char * *, const char *
        self.__lib.alljoyn_aboutdata_getappname.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_getappname.argtypes = [C.c_void_p, POINTER(C.c_char_p), C.c_char_p]
        return QStatus(self.__lib.alljoyn_aboutdata_getappname(data, appName, language)) 


    # wrapper for alljoyn_aboutdata_setmanufacturer returns QStatus
    def AboutdataSetmanufacturer(self, data, manufacturer, language):  # alljoyn_aboutdata, const char *, const char *
        self.__lib.alljoyn_aboutdata_setmanufacturer.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_setmanufacturer.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_aboutdata_setmanufacturer(data, manufacturer, language)) 


    # wrapper for alljoyn_aboutdata_getmanufacturer returns QStatus
    def AboutdataGetmanufacturer(self, data, manufacturer, language):  # alljoyn_aboutdata, char * *, const char *
        self.__lib.alljoyn_aboutdata_getmanufacturer.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_getmanufacturer.argtypes = [C.c_void_p, POINTER(C.c_char_p), C.c_char_p]
        return QStatus(self.__lib.alljoyn_aboutdata_getmanufacturer(data, manufacturer, language)) 


    # wrapper for alljoyn_aboutdata_setmodelnumber returns QStatus
    def AboutdataSetmodelnumber(self, data, modelNumber):  # alljoyn_aboutdata, const char *
        self.__lib.alljoyn_aboutdata_setmodelnumber.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_setmodelnumber.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_aboutdata_setmodelnumber(data, modelNumber)) 


    # wrapper for alljoyn_aboutdata_getmodelnumber returns QStatus
    def AboutdataGetmodelnumber(self, data, modelNumber):  # alljoyn_aboutdata, char * *
        self.__lib.alljoyn_aboutdata_getmodelnumber.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_getmodelnumber.argtypes = [C.c_void_p, POINTER(C.c_char_p)]
        return QStatus(self.__lib.alljoyn_aboutdata_getmodelnumber(data, modelNumber)) 


    # wrapper for alljoyn_aboutdata_setsupportedlanguage returns QStatus
    def AboutdataSetsupportedlanguage(self, data, language):  # alljoyn_aboutdata, const char *
        self.__lib.alljoyn_aboutdata_setsupportedlanguage.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_setsupportedlanguage.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_aboutdata_setsupportedlanguage(data, language)) 


    # wrapper for alljoyn_aboutdata_getsupportedlanguages returns size_t
    def AboutdataGetsupportedlanguages(self, data, languageTags, num):  # alljoyn_aboutdata, const char * *, size_t
        self.__lib.alljoyn_aboutdata_getsupportedlanguages.restype = C.c_size_t
        self.__lib.alljoyn_aboutdata_getsupportedlanguages.argtypes = [C.c_void_p, POINTER(C.c_char_p), C.csize_t]
        return self.__lib.alljoyn_aboutdata_getsupportedlanguages(data, languageTags, num) 


    # wrapper for alljoyn_aboutdata_setdescription returns QStatus
    def AboutdataSetdescription(self, data, description, language):  # alljoyn_aboutdata, const char *, const char *
        self.__lib.alljoyn_aboutdata_setdescription.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_setdescription.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_aboutdata_setdescription(data, description, language)) 


    # wrapper for alljoyn_aboutdata_getdescription returns QStatus
    def AboutdataGetdescription(self, data, description, language):  # alljoyn_aboutdata, char * *, const char *
        self.__lib.alljoyn_aboutdata_getdescription.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_getdescription.argtypes = [C.c_void_p, POINTER(C.c_char_p), C.c_char_p]
        return QStatus(self.__lib.alljoyn_aboutdata_getdescription(data, description, language)) 


    # wrapper for alljoyn_aboutdata_setdateofmanufacture returns QStatus
    def AboutdataSetdateofmanufacture(self, data, dateOfManufacture):  # alljoyn_aboutdata, const char *
        self.__lib.alljoyn_aboutdata_setdateofmanufacture.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_setdateofmanufacture.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_aboutdata_setdateofmanufacture(data, dateOfManufacture)) 


    # wrapper for alljoyn_aboutdata_getdateofmanufacture returns QStatus
    def AboutdataGetdateofmanufacture(self, data, dateOfManufacture):  # alljoyn_aboutdata, char * *
        self.__lib.alljoyn_aboutdata_getdateofmanufacture.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_getdateofmanufacture.argtypes = [C.c_void_p, POINTER(C.c_char_p)]
        return QStatus(self.__lib.alljoyn_aboutdata_getdateofmanufacture(data, dateOfManufacture)) 


    # wrapper for alljoyn_aboutdata_setsoftwareversion returns QStatus
    def AboutdataSetsoftwareversion(self, data, softwareVersion):  # alljoyn_aboutdata, const char *
        self.__lib.alljoyn_aboutdata_setsoftwareversion.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_setsoftwareversion.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_aboutdata_setsoftwareversion(data, softwareVersion)) 


    # wrapper for alljoyn_aboutdata_getsoftwareversion returns QStatus
    def AboutdataGetsoftwareversion(self, data, softwareVersion):  # alljoyn_aboutdata, char * *
        self.__lib.alljoyn_aboutdata_getsoftwareversion.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_getsoftwareversion.argtypes = [C.c_void_p, POINTER(C.c_char_p)]
        return QStatus(self.__lib.alljoyn_aboutdata_getsoftwareversion(data, softwareVersion)) 


    # wrapper for alljoyn_aboutdata_getajsoftwareversion returns QStatus
    def AboutdataGetajsoftwareversion(self, data, ajSoftwareVersion):  # alljoyn_aboutdata, char * *
        self.__lib.alljoyn_aboutdata_getajsoftwareversion.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_getajsoftwareversion.argtypes = [C.c_void_p, POINTER(C.c_char_p)]
        return QStatus(self.__lib.alljoyn_aboutdata_getajsoftwareversion(data, ajSoftwareVersion)) 


    # wrapper for alljoyn_aboutdata_sethardwareversion returns QStatus
    def AboutdataSethardwareversion(self, data, hardwareVersion):  # alljoyn_aboutdata, const char *
        self.__lib.alljoyn_aboutdata_sethardwareversion.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_sethardwareversion.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_aboutdata_sethardwareversion(data, hardwareVersion)) 


    # wrapper for alljoyn_aboutdata_gethardwareversion returns QStatus
    def AboutdataGethardwareversion(self, data, hardwareVersion):  # alljoyn_aboutdata, char * *
        self.__lib.alljoyn_aboutdata_gethardwareversion.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_gethardwareversion.argtypes = [C.c_void_p, POINTER(C.c_char_p)]
        return QStatus(self.__lib.alljoyn_aboutdata_gethardwareversion(data, hardwareVersion)) 


    # wrapper for alljoyn_aboutdata_setsupporturl returns QStatus
    def AboutdataSetsupporturl(self, data, supportUrl):  # alljoyn_aboutdata, const char *
        self.__lib.alljoyn_aboutdata_setsupporturl.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_setsupporturl.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_aboutdata_setsupporturl(data, supportUrl)) 


    # wrapper for alljoyn_aboutdata_getsupporturl returns QStatus
    def AboutdataGetsupporturl(self, data, supportUrl):  # alljoyn_aboutdata, char * *
        self.__lib.alljoyn_aboutdata_getsupporturl.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_getsupporturl.argtypes = [C.c_void_p, POINTER(C.c_char_p)]
        return QStatus(self.__lib.alljoyn_aboutdata_getsupporturl(data, supportUrl)) 


    # wrapper for alljoyn_aboutdata_setfield returns QStatus
    def AboutdataSetfield(self, data, name, value, language):  # alljoyn_aboutdata, const char *, alljoyn_msgarg, const char *
        self.__lib.alljoyn_aboutdata_setfield.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_setfield.argtypes = [C.c_void_p, C.c_char_p, C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_aboutdata_setfield(data, name, value, language)) 


    # wrapper for alljoyn_aboutdata_getfields returns size_t
    def AboutdataGetfields(self, data, fields, num_fields):  # alljoyn_aboutdata, const char * *, size_t
        self.__lib.alljoyn_aboutdata_getfields.restype = C.c_size_t
        self.__lib.alljoyn_aboutdata_getfields.argtypes = [C.c_void_p, POINTER(C.c_char_p), C.csize_t]
        return self.__lib.alljoyn_aboutdata_getfields(data, fields, num_fields) 


    # wrapper for alljoyn_aboutdata_getaboutdata returns QStatus
    def AboutdataGetaboutdata(self, data, msgArg, language):  # alljoyn_aboutdata, alljoyn_msgarg, const char *
        self.__lib.alljoyn_aboutdata_getaboutdata.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_getaboutdata.argtypes = [C.c_void_p, C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_aboutdata_getaboutdata(data, msgArg, language)) 


    # wrapper for alljoyn_aboutdata_getannouncedaboutdata returns QStatus
    def AboutdataGetannouncedaboutdata(self, data, msgArg):  # alljoyn_aboutdata, alljoyn_msgarg
        self.__lib.alljoyn_aboutdata_getannouncedaboutdata.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_getannouncedaboutdata.argtypes = [C.c_void_p, C.c_void_p]
        return QStatus(self.__lib.alljoyn_aboutdata_getannouncedaboutdata(data, msgArg)) 


    # wrapper for alljoyn_aboutdata_isfieldrequired returns bool
    def AboutdataIsfieldrequired(self, data, fieldName):  # alljoyn_aboutdata, const char *
        self.__lib.alljoyn_aboutdata_isfieldrequired.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_isfieldrequired.argtypes = [C.c_void_p, C.c_char_p]
        return self.__lib.alljoyn_aboutdata_isfieldrequired(data, fieldName) 


    # wrapper for alljoyn_aboutdata_isfieldannounced returns bool
    def AboutdataIsfieldannounced(self, data, fieldName):  # alljoyn_aboutdata, const char *
        self.__lib.alljoyn_aboutdata_isfieldannounced.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_isfieldannounced.argtypes = [C.c_void_p, C.c_char_p]
        return self.__lib.alljoyn_aboutdata_isfieldannounced(data, fieldName) 


    # wrapper for alljoyn_aboutdata_isfieldlocalized returns bool
    def AboutdataIsfieldlocalized(self, data, fieldName):  # alljoyn_aboutdata, const char *
        self.__lib.alljoyn_aboutdata_isfieldlocalized.restype = C.c_uint
        self.__lib.alljoyn_aboutdata_isfieldlocalized.argtypes = [C.c_void_p, C.c_char_p]
        return self.__lib.alljoyn_aboutdata_isfieldlocalized(data, fieldName) 


    # wrapper for alljoyn_aboutdata_getfieldsignature returns const char *
    def AboutdataGetfieldsignature(self, data, fieldName):  # alljoyn_aboutdata, const char *
        self.__lib.alljoyn_aboutdata_getfieldsignature.restype = C.c_char_p
        self.__lib.alljoyn_aboutdata_getfieldsignature.argtypes = [C.c_void_p, C.c_char_p]
        return self.__lib.alljoyn_aboutdata_getfieldsignature(data, fieldName) 



class AboutObj(object):
    
    __metaclass__ = AllJoynMeta
    
    
    # wrapper for alljoyn_aboutobj_destroy returns void
    def AboutobjDestroy(self, obj):  # alljoyn_aboutobj
        self.__lib.alljoyn_aboutobj_destroy.argtypes = [C.c_void_p]
        self.__lib.alljoyn_aboutobj_destroy(obj) 


    # wrapper for alljoyn_aboutobj_announce returns QStatus
    def AboutobjAnnounce(self, obj, sessionPort, aboutData):  # alljoyn_aboutobj, alljoyn_sessionport, alljoyn_aboutdata
        self.__lib.alljoyn_aboutobj_announce.restype = C.c_uint
        self.__lib.alljoyn_aboutobj_announce.argtypes = [C.c_void_p, C.c_uint16, C.c_void_p]
        return QStatus(self.__lib.alljoyn_aboutobj_announce(obj, sessionPort, aboutData)) 


    # wrapper for alljoyn_aboutobj_unannounce returns QStatus
    def AboutobjUnannounce(self, obj):  # alljoyn_aboutobj
        self.__lib.alljoyn_aboutobj_unannounce.restype = C.c_uint
        self.__lib.alljoyn_aboutobj_unannounce.argtypes = [C.c_void_p]
        return QStatus(self.__lib.alljoyn_aboutobj_unannounce(obj)) 
    
    
class AboutObjectDescription(object):
    
    __metaclass__ = AllJoynMeta
    
    def __init__(self, alljoyn_msgarg):
        self.handle = self.AboutobjectdescriptionCreate(alljoyn_msgarg)
    
    def __del__(self):
        self.AboutobjectdescriptionDestroy(self.handle)
    
    def CreateFromMsgArg(self, description, arg):
        return self.AboutobjectdescriptionCreatefrommsgarg(description, arg)
            
    def Getpaths(self, paths, numPaths):
        return self.AboutobjectdescriptionGetpaths(self.handle, paths, numPaths)
            
    def GetInterfaces(self, path, interfaces, numInterfaces):
        return self.AboutobjectdescriptionGetinterfaces(self.handle, path, interfaces, numInterfaces)
            
                  
            
            
            
    # wrapper for alljoyn_aboutobjectdescription_create returns alljoyn_aboutobjectdescription
    def AboutobjectdescriptionCreate(self, alljoyn_msgarg):  # const alljoyn_msgarg
        self.__lib.alljoyn_aboutobjectdescription_create.restype = C.c_void_p
        self.__lib.alljoyn_aboutobjectdescription_create.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_aboutobjectdescription_create(alljoyn_msgarg) 
    
    # wrapper for alljoyn_aboutobjectdescription_create_full returns alljoyn_aboutobjectdescription
    def AboutobjectdescriptionCreateFull(self, arg):  # const alljoyn_msgarg
        self.__lib.alljoyn_aboutobjectdescription_create_full.restype = C.c_void_p
        self.__lib.alljoyn_aboutobjectdescription_create_full.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_aboutobjectdescription_create_full(arg) 


    # wrapper for alljoyn_aboutobjectdescription_createfrommsgarg returns QStatus
    def AboutobjectdescriptionCreatefrommsgarg(self, description, arg):  # alljoyn_aboutobjectdescription, const alljoyn_msgarg
        self.__lib.alljoyn_aboutobjectdescription_createfrommsgarg.restype = C.c_uint
        self.__lib.alljoyn_aboutobjectdescription_createfrommsgarg.argtypes = [C.c_void_p, C.c_void_p]
        return QStatus(self.__lib.alljoyn_aboutobjectdescription_createfrommsgarg(description, arg)) 


    # wrapper for alljoyn_aboutobjectdescription_destroy returns void
    def AboutobjectdescriptionDestroy(self, description):  # alljoyn_aboutobjectdescription
        self.__lib.alljoyn_aboutobjectdescription_destroy.argtypes = [C.c_void_p]
        self.__lib.alljoyn_aboutobjectdescription_destroy(description) 


    # wrapper for alljoyn_aboutobjectdescription_getpaths returns size_t
    def AboutobjectdescriptionGetpaths(self, description, paths, numPaths):  # alljoyn_aboutobjectdescription, const char * *, size_t
        self.__lib.alljoyn_aboutobjectdescription_getpaths.restype = C.c_size_t
        self.__lib.alljoyn_aboutobjectdescription_getpaths.argtypes = [C.c_void_p, POINTER(C.c_char_p), C.csize_t]
        return self.__lib.alljoyn_aboutobjectdescription_getpaths(description, paths, numPaths) 


    # wrapper for alljoyn_aboutobjectdescription_getinterfaces returns size_t
    def AboutobjectdescriptionGetinterfaces(self, description, path, interfaces, numInterfaces):  # alljoyn_aboutobjectdescription, const char *, const char * *, size_t
        self.__lib.alljoyn_aboutobjectdescription_getinterfaces.restype = C.c_size_t
        self.__lib.alljoyn_aboutobjectdescription_getinterfaces.argtypes = [C.c_void_p, C.c_char_p, POINTER(C.c_char_p), C.csize_t]
        return self.__lib.alljoyn_aboutobjectdescription_getinterfaces(description, path, interfaces, numInterfaces) 


    # wrapper for alljoyn_aboutobjectdescription_getinterfacepaths returns size_t
    def AboutobjectdescriptionGetinterfacepaths(self, description, interfaceName, paths, numPaths):  # alljoyn_aboutobjectdescription, const char *, const char * *, size_t
        self.__lib.alljoyn_aboutobjectdescription_getinterfacepaths.restype = C.c_size_t
        self.__lib.alljoyn_aboutobjectdescription_getinterfacepaths.argtypes = [C.c_void_p, C.c_char_p, POINTER(C.c_char_p), C.csize_t]
        return self.__lib.alljoyn_aboutobjectdescription_getinterfacepaths(description, interfaceName, paths, numPaths) 


    # wrapper for alljoyn_aboutobjectdescription_clear returns void
    def AboutobjectdescriptionClear(self, description):  # alljoyn_aboutobjectdescription
        self.__lib.alljoyn_aboutobjectdescription_clear.argtypes = [C.c_void_p]
        self.__lib.alljoyn_aboutobjectdescription_clear(description) 


    # wrapper for alljoyn_aboutobjectdescription_haspath returns bool
    def AboutobjectdescriptionHaspath(self, description, path):  # alljoyn_aboutobjectdescription, const char *
        self.__lib.alljoyn_aboutobjectdescription_haspath.restype = C.c_uint
        self.__lib.alljoyn_aboutobjectdescription_haspath.argtypes = [C.c_void_p, C.c_char_p]
        return self.__lib.alljoyn_aboutobjectdescription_haspath(description, path) 


    # wrapper for alljoyn_aboutobjectdescription_hasinterface returns bool
    def AboutobjectdescriptionHasinterface(self, description, interfaceName):  # alljoyn_aboutobjectdescription, const char *
        self.__lib.alljoyn_aboutobjectdescription_hasinterface.restype = C.c_uint
        self.__lib.alljoyn_aboutobjectdescription_hasinterface.argtypes = [C.c_void_p, C.c_char_p]
        return self.__lib.alljoyn_aboutobjectdescription_hasinterface(description, interfaceName) 


    # wrapper for alljoyn_aboutobjectdescription_hasinterfaceatpath returns bool
    def AboutobjectdescriptionHasinterfaceatpath(self, description, path, interfaceName):  # alljoyn_aboutobjectdescription, const char *, const char *
        self.__lib.alljoyn_aboutobjectdescription_hasinterfaceatpath.restype = C.c_uint
        self.__lib.alljoyn_aboutobjectdescription_hasinterfaceatpath.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p]
        return self.__lib.alljoyn_aboutobjectdescription_hasinterfaceatpath(description, path, interfaceName) 


    # wrapper for alljoyn_aboutobjectdescription_getmsgarg returns QStatus
    def AboutobjectdescriptionGetmsgarg(self, description, msgArg):  # alljoyn_aboutobjectdescription, alljoyn_msgarg
        self.__lib.alljoyn_aboutobjectdescription_getmsgarg.restype = C.c_uint
        self.__lib.alljoyn_aboutobjectdescription_getmsgarg.argtypes = [C.c_void_p, C.c_void_p]
        return QStatus(self.__lib.alljoyn_aboutobjectdescription_getmsgarg(description, msgArg)) 
    


class AboutProxy(object):
    
    __metaclass__ = AllJoynMeta
    
    
        # wrapper for alljoyn_aboutproxy_create returns alljoyn_aboutproxy
    def AboutproxyCreate(self, bus, busName, sessionId):  # alljoyn_busattachment, const char *, alljoyn_sessionid
        self.__lib.alljoyn_aboutproxy_create.restype = C.c_void_p
        self.__lib.alljoyn_aboutproxy_create.argtypes = [C.c_void_p, C.c_char_p, C.c_uint32]
        return self.__lib.alljoyn_aboutproxy_create(bus, busName, sessionId) 


    # wrapper for alljoyn_aboutproxy_destroy returns void
    def AboutproxyDestroy(self, proxy):  # alljoyn_aboutproxy
        self.__lib.alljoyn_aboutproxy_destroy.argtypes = [C.c_void_p]
        self.__lib.alljoyn_aboutproxy_destroy(proxy) 


    # wrapper for alljoyn_aboutproxy_getobjectdescription returns QStatus
    def AboutproxyGetobjectdescription(self, proxy, objectDesc):  # alljoyn_aboutproxy, alljoyn_msgarg
        self.__lib.alljoyn_aboutproxy_getobjectdescription.restype = C.c_uint
        self.__lib.alljoyn_aboutproxy_getobjectdescription.argtypes = [C.c_void_p, C.c_void_p]
        return QStatus(self.__lib.alljoyn_aboutproxy_getobjectdescription(proxy, objectDesc)) 


    # wrapper for alljoyn_aboutproxy_getaboutdata returns QStatus
    def AboutproxyGetaboutdata(self, proxy, language, data):  # alljoyn_aboutproxy, const char *, alljoyn_msgarg
        self.__lib.alljoyn_aboutproxy_getaboutdata.restype = C.c_uint
        self.__lib.alljoyn_aboutproxy_getaboutdata.argtypes = [C.c_void_p, C.c_char_p, C.c_void_p]
        return QStatus(self.__lib.alljoyn_aboutproxy_getaboutdata(proxy, language, data)) 


    # wrapper for alljoyn_aboutproxy_getversion returns QStatus
    def AboutproxyGetversion(self, proxy, version):  # alljoyn_aboutproxy, uint16_t *
        self.__lib.alljoyn_aboutproxy_getversion.restype = C.c_uint
        self.__lib.alljoyn_aboutproxy_getversion.argtypes = [C.c_void_p, POINTER(C.c_uint16)]
        return QStatus(self.__lib.alljoyn_aboutproxy_getversion(proxy, version)) 


class AboutIcon(object):
        # wrapper for alljoyn_abouticon_destroy returns void
    def AbouticonDestroy(self, icon):  # alljoyn_abouticon
        self.__lib.alljoyn_abouticon_destroy.argtypes = [C.c_void_p]
        self.__lib.alljoyn_abouticon_destroy(icon) 


    # wrapper for alljoyn_abouticon_getcontent returns void
    def AbouticonGetcontent(self, icon, data, size):  # alljoyn_abouticon, const uint8_t * *, size_t *
        self.__lib.alljoyn_abouticon_getcontent.argtypes = [C.c_void_p, POINTER(C.c_uint8), POINTER(C.csize_t)]
        self.__lib.alljoyn_abouticon_getcontent(icon, data, size) 


    # wrapper for alljoyn_abouticon_setcontent returns QStatus
    def AbouticonSetcontent(self, icon, type, data, csize, ownsData):  # alljoyn_abouticon, const char *, uint8_t *, size_t, bool
        self.__lib.alljoyn_abouticon_setcontent.restype = C.c_uint
        self.__lib.alljoyn_abouticon_setcontent.argtypes = [C.c_void_p, C.c_char_p, POINTER(C.c_uint8_t), C.csize_t, C.c_uint8]
        return QStatus(self.__lib.alljoyn_abouticon_setcontent(icon, type, data, csize, ownsData)) 


    # wrapper for alljoyn_abouticon_geturl returns void
    def AbouticonGeturl(self, icon, type, url):  # alljoyn_abouticon, const char * *, const char * *
        self.__lib.alljoyn_abouticon_geturl.argtypes = [C.c_void_p, POINTER(C.c_char_p), POINTER(C.c_char_p)]
        self.__lib.alljoyn_abouticon_geturl(icon, type, url) 


    # wrapper for alljoyn_abouticon_seturl returns QStatus
    def AbouticonSeturl(self, icon, type, url):  # alljoyn_abouticon, const char *, const char *
        self.__lib.alljoyn_abouticon_seturl.restype = C.c_uint
        self.__lib.alljoyn_abouticon_seturl.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_abouticon_seturl(icon, type, url)) 


    # wrapper for alljoyn_abouticon_clear returns void
    def AbouticonClear(self, icon):  # alljoyn_abouticon
        self.__lib.alljoyn_abouticon_clear.argtypes = [C.c_void_p]
        self.__lib.alljoyn_abouticon_clear(icon) 


    # wrapper for alljoyn_abouticon_setcontent_frommsgarg returns QStatus
    def AbouticonSetcontentFrommsgarg(self, icon, arg):  # alljoyn_abouticon, const alljoyn_msgarg
        self.__lib.alljoyn_abouticon_setcontent_frommsgarg.restype = C.c_uint
        self.__lib.alljoyn_abouticon_setcontent_frommsgarg.argtypes = [C.c_void_p, C.c_void_p]
        return QStatus(self.__lib.alljoyn_abouticon_setcontent_frommsgarg(icon, arg)) 



class AboutIconObj(object):
    
    __metaclass__ = AllJoynMeta
    
    # wrapper for alljoyn_abouticonobj_create returns alljoyn_abouticonobj
    def AbouticonobjCreate(self, bus, icon):  # alljoyn_busattachment, alljoyn_abouticon
        self.__lib.alljoyn_abouticonobj_create.restype = C.c_void_p
        self.__lib.alljoyn_abouticonobj_create.argtypes = [C.c_void_p, C.c_void_p]
        return self.__lib.alljoyn_abouticonobj_create(bus, icon) 
        
        
class AboutIconProxy(object):
    
    __metaclass__ = AllJoynMeta
    
        # wrapper for alljoyn_abouticonproxy_create returns alljoyn_abouticonproxy
    def AbouticonproxyCreate(self, bus, busName, sessionId):  # alljoyn_busattachment, const char *, alljoyn_sessionid
        self.__lib.alljoyn_abouticonproxy_create.restype = C.c_void_p
        self.__lib.alljoyn_abouticonproxy_create.argtypes = [C.c_void_p, C.c_char_p, C.c_uint32]
        return self.__lib.alljoyn_abouticonproxy_create(bus, busName, sessionId) 


    # wrapper for alljoyn_abouticonproxy_destroy returns void
    def AbouticonproxyDestroy(self, proxy):  # alljoyn_abouticonproxy
        self.__lib.alljoyn_abouticonproxy_destroy.argtypes = [C.c_void_p]
        self.__lib.alljoyn_abouticonproxy_destroy(proxy) 


    # wrapper for alljoyn_abouticonproxy_geticon returns QStatus
    def AbouticonproxyGeticon(self, proxy, icon):  # alljoyn_abouticonproxy, alljoyn_abouticon
        self.__lib.alljoyn_abouticonproxy_geticon.restype = C.c_uint
        self.__lib.alljoyn_abouticonproxy_geticon.argtypes = [C.c_void_p, C.c_void_p]
        return QStatus(self.__lib.alljoyn_abouticonproxy_geticon(proxy, icon)) 


    # wrapper for alljoyn_abouticonproxy_getversion returns QStatus
    def AbouticonproxyGetversion(self, proxy, version):  # alljoyn_abouticonproxy, uint16_t *
        self.__lib.alljoyn_abouticonproxy_getversion.restype = C.c_uint
        self.__lib.alljoyn_abouticonproxy_getversion.argtypes = [C.c_void_p, POINTER(C.c_uint16)]
        return QStatus(self.__lib.alljoyn_abouticonproxy_getversion(proxy, version)) 

   

class BusAttachment(object):
    
    __metaclass__ = AllJoynMeta
    
    def __init__(self, application_name, allow_remote_mesages=Constants.QCC_TRUE):
        self.handle = self.BusattachmentCreate(application_name, allow_remote_mesages)
    
    def __del__(self):
        self.BusattachmentDestroy(self.handle)
        
    def Start(self):
        return self.BusattachmentStart(self.handle)
    
    def Connect(connectSpec):
        self.BusattachmentConnect(self.handle, connectSpec)
    
    def GetUniqueName():
        self.BusattachmentGetuniquename(self.handle)
    
    # wrapper for alljoyn_busattachment_create returns alljoyn_busattachment
    def BusattachmentCreate(self, applicationName, allowRemoteMessages):  # const char *, QCC_BOOL
        self.__lib.alljoyn_busattachment_create.restype = C.c_void_p
        self.__lib.alljoyn_busattachment_create.argtypes = [C.c_char_p, C.c_int32]
        return C.c_void_p(self.__lib.alljoyn_busattachment_create(applicationName, allowRemoteMessages))


    # wrapper for alljoyn_busattachment_create_concurrency returns alljoyn_busattachment
    def BusattachmentCreateConcurrency(self, applicationName, allowRemoteMessages, concurrency):  # const char *, QCC_BOOL, uint32_t
        self.__lib.alljoyn_busattachment_create_concurrency.restype = C.c_void_p
        self.__lib.alljoyn_busattachment_create_concurrency.argtypes = [C.c_char_p, C.c_uint8, C.uint32_t]
        return self.__lib.alljoyn_busattachment_create_concurrency(applicationName, allowRemoteMessages, concurrency) 


    # wrapper for alljoyn_busattachment_destroy returns void
    def BusattachmentDestroy(self, bus):  # alljoyn_busattachment
        self.__lib.alljoyn_busattachment_destroy.argtypes = [C.c_void_p]
        self.__lib.alljoyn_busattachment_destroy(bus) 


    # wrapper for alljoyn_busattachment_start returns QStatus
    def BusattachmentStart(self, bus):  # alljoyn_busattachment
        self.__lib.alljoyn_busattachment_start.restype = C.c_uint
        self.__lib.alljoyn_busattachment_start.argtypes = [C.c_void_p]
        return QStatus(self.__lib.alljoyn_busattachment_start(bus)) 


    # wrapper for alljoyn_busattachment_stop returns QStatus
    def BusattachmentStop(self, bus):  # alljoyn_busattachment
        self.__lib.alljoyn_busattachment_stop.restype = C.c_uint
        self.__lib.alljoyn_busattachment_stop.argtypes = [C.c_void_p]
        return QStatus(self.__lib.alljoyn_busattachment_stop(bus)) 


    # wrapper for alljoyn_busattachment_join returns QStatus
    def BusattachmentJoin(self, bus):  # alljoyn_busattachment
        self.__lib.alljoyn_busattachment_join.restype = C.c_uint
        self.__lib.alljoyn_busattachment_join.argtypes = [C.c_void_p]
        return QStatus(self.__lib.alljoyn_busattachment_join(bus)) 


    # wrapper for alljoyn_busattachment_getconcurrency returns uint32_t
    def BusattachmentGetconcurrency(self, bus):  # alljoyn_busattachment
        self.__lib.alljoyn_busattachment_getconcurrency.restype = C.c_uint32
        self.__lib.alljoyn_busattachment_getconcurrency.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_busattachment_getconcurrency(bus) 


    # wrapper for alljoyn_busattachment_getconnectspec returns const char *
    def BusattachmentGetconnectspec(self, bus):  # alljoyn_busattachment
        self.__lib.alljoyn_busattachment_getconnectspec.restype = C.c_char_p
        self.__lib.alljoyn_busattachment_getconnectspec.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_busattachment_getconnectspec(bus) 


    # wrapper for alljoyn_busattachment_enableconcurrentcallbacks returns void
    def BusattachmentEnableconcurrentcallbacks(self, bus):  # alljoyn_busattachment
        self.__lib.alljoyn_busattachment_enableconcurrentcallbacks.argtypes = [C.c_void_p]
        self.__lib.alljoyn_busattachment_enableconcurrentcallbacks(bus) 


    # wrapper for alljoyn_busattachment_createinterface returns QStatus
    def BusattachmentCreateinterface(self, bus, name, iface):  # alljoyn_busattachment, const char *, alljoyn_interfacedescription *
        self.__lib.alljoyn_busattachment_createinterface.restype = C.c_uint
        self.__lib.alljoyn_busattachment_createinterface.argtypes = [C.c_void_p, C.c_char_p, POINTER(C.c_void_p)]
        return QStatus(self.__lib.alljoyn_busattachment_createinterface(bus, name, iface)) 


    # wrapper for alljoyn_busattachment_connect returns QStatus
    def BusattachmentConnect(self, bus, connectSpec):  # alljoyn_busattachment_connect, const char *
        self.__lib.alljoyn_busattachment_connect.restype = C.c_uint
        self.__lib.alljoyn_busattachment_connect.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_busattachment_connect(bus, connectSpec)) 


    # wrapper for alljoyn_busattachment_registerbuslistener returns void
    def BusattachmentRegisterbuslistener(self, bus, listener):  # alljoyn_busattachment, alljoyn_buslistener
        self.__lib.alljoyn_busattachment_registerbuslistener.argtypes = [C.c_void_p, C.c_void_p]
        self.__lib.alljoyn_busattachment_registerbuslistener(bus, listener) 


    # wrapper for alljoyn_busattachment_unregisterbuslistener returns void
    def BusattachmentUnregisterbuslistener(self, bus, listener):  # alljoyn_busattachment, alljoyn_buslistener
        self.__lib.alljoyn_busattachment_unregisterbuslistener.argtypes = [C.c_void_p, C.c_void_p]
        self.__lib.alljoyn_busattachment_unregisterbuslistener(bus, listener) 


    # wrapper for alljoyn_busattachment_findadvertisedname returns QStatus
    def BusattachmentFindadvertisedname(self, bus, namePrefix):  # alljoyn_busattachment, const char *
        self.__lib.alljoyn_busattachment_findadvertisedname.restype = C.c_uint
        self.__lib.alljoyn_busattachment_findadvertisedname.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_busattachment_findadvertisedname(bus, namePrefix)) 


    # wrapper for alljoyn_busattachment_findadvertisednamebytransport returns QStatus
    def BusattachmentFindadvertisednamebytransport(self, bus, namePrefix, transports):  # alljoyn_busattachment, const char *, alljoyn_transportmask
        self.__lib.alljoyn_busattachment_findadvertisednamebytransport.restype = C.c_uint
        self.__lib.alljoyn_busattachment_findadvertisednamebytransport.argtypes = [C.c_void_p, C.c_char_p, C.c_void_p]
        return QStatus(self.__lib.alljoyn_busattachment_findadvertisednamebytransport(bus, namePrefix, transports)) 


    # wrapper for alljoyn_busattachment_cancelfindadvertisedname returns QStatus
    def BusattachmentCancelfindadvertisedname(self, bus, namePrefix):  # alljoyn_busattachment, const char *
        self.__lib.alljoyn_busattachment_cancelfindadvertisedname.restype = C.c_uint
        self.__lib.alljoyn_busattachment_cancelfindadvertisedname.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_busattachment_cancelfindadvertisedname(bus, namePrefix)) 


    # wrapper for alljoyn_busattachment_cancelfindadvertisednamebytransport returns QStatus
    def BusattachmentCancelfindadvertisednamebytransport(self, bus, namePrefix, transports):  # alljoyn_busattachment, const char *, alljoyn_transportmask
        self.__lib.alljoyn_busattachment_cancelfindadvertisednamebytransport.restype = C.c_uint
        self.__lib.alljoyn_busattachment_cancelfindadvertisednamebytransport.argtypes = [C.c_void_p, C.c_char_p, C.c_void_p]
        return QStatus(self.__lib.alljoyn_busattachment_cancelfindadvertisednamebytransport(bus, namePrefix, transports)) 


    # wrapper for alljoyn_busattachment_advertisename returns QStatus
    def BusattachmentAdvertisename(self, bus, name, transports):  # alljoyn_busattachment, const char *, alljoyn_transportmask
        self.__lib.alljoyn_busattachment_advertisename.restype = C.c_uint
        self.__lib.alljoyn_busattachment_advertisename.argtypes = [C.c_void_p, C.c_char_p, C.c_void_p]
        return QStatus(self.__lib.alljoyn_busattachment_advertisename(bus, name, transports)) 


    # wrapper for alljoyn_busattachment_canceladvertisename returns QStatus
    def BusattachmentCanceladvertisename(self, bus, name, transports):  # alljoyn_busattachment, const char *, alljoyn_transportmask
        self.__lib.alljoyn_busattachment_canceladvertisename.restype = C.c_uint
        self.__lib.alljoyn_busattachment_canceladvertisename.argtypes = [C.c_void_p, C.c_char_p, C.c_void_p]
        return QStatus(self.__lib.alljoyn_busattachment_canceladvertisename(bus, name, transports)) 


    # wrapper for alljoyn_busattachment_getinterface returns const alljoyn_interfacedescription
    def BusattachmentGetinterface(self, bus, name):  # alljoyn_busattachment, const char *
        self.__lib.alljoyn_busattachment_getinterface.restype = C.c_void_p
        self.__lib.alljoyn_busattachment_getinterface.argtypes = [C.c_void_p, C.c_char_p]
        return self.__lib.alljoyn_busattachment_getinterface(bus, name) 


    # wrapper for alljoyn_busattachment_registerbusobject returns QStatus
    def BusattachmentRegisterbusobject(self, bus, obj):  # alljoyn_busattachment, alljoyn_busobject
        self.__lib.alljoyn_busattachment_registerbusobject.restype = C.c_uint
        self.__lib.alljoyn_busattachment_registerbusobject.argtypes = [C.c_void_p, C.c_void_p]
        return QStatus(self.__lib.alljoyn_busattachment_registerbusobject(bus, obj)) 


    # wrapper for alljoyn_busattachment_registerbusobject_secure returns QStatus
    def BusattachmentRegisterbusobjectSecure(self, bus, obj):  # alljoyn_busattachment, alljoyn_busobject
        self.__lib.alljoyn_busattachment_registerbusobject_secure.restype = C.c_uint
        self.__lib.alljoyn_busattachment_registerbusobject_secure.argtypes = [C.c_void_p, C.c_void_p]
        return QStatus(self.__lib.alljoyn_busattachment_registerbusobject_secure(bus, obj)) 


    # wrapper for alljoyn_busattachment_unregisterbusobject returns void
    def BusattachmentUnregisterbusobject(self, bus, object):  # alljoyn_busattachment, alljoyn_busobject
        self.__lib.alljoyn_busattachment_unregisterbusobject.argtypes = [C.c_void_p, C.c_void_p]
        self.__lib.alljoyn_busattachment_unregisterbusobject(bus, object) 


    # wrapper for alljoyn_busattachment_requestname returns QStatus
    def BusattachmentRequestname(self, bus, requestedName, flags):  # alljoyn_busattachment, const char *, uint32_t
        self.__lib.alljoyn_busattachment_requestname.restype = C.c_uint
        self.__lib.alljoyn_busattachment_requestname.argtypes = [C.c_void_p, C.c_char_p, C.uint32_t]
        return QStatus(self.__lib.alljoyn_busattachment_requestname(bus, requestedName, flags)) 


    # wrapper for alljoyn_busattachment_releasename returns QStatus
    def BusattachmentReleasename(self, bus, name):  # alljoyn_busattachment, const char *
        self.__lib.alljoyn_busattachment_releasename.restype = C.c_uint
        self.__lib.alljoyn_busattachment_releasename.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_busattachment_releasename(bus, name)) 


    # wrapper for alljoyn_busattachment_unbindsessionport returns QStatus
    def BusattachmentUnbindsessionport(self, bus, sessionPort):  # alljoyn_busattachment, alljoyn_sessionport
        self.__lib.alljoyn_busattachment_unbindsessionport.restype = C.c_uint
        self.__lib.alljoyn_busattachment_unbindsessionport.argtypes = [C.c_void_p, C.c_uint16]
        return QStatus(self.__lib.alljoyn_busattachment_unbindsessionport(bus, sessionPort)) 


    # wrapper for alljoyn_busattachment_enablepeersecurity returns QStatus
    def BusattachmentEnablepeersecurity(self, bus, authMechanisms, listener, keyStoreFileName, isShared):  # alljoyn_busattachment, const char *, alljoyn_authlistener, const char *, QCC_BOOL
        self.__lib.alljoyn_busattachment_enablepeersecurity.restype = C.c_uint
        self.__lib.alljoyn_busattachment_enablepeersecurity.argtypes = [C.c_void_p, C.c_char_p, C.c_void_p, C.c_char_p, C.c_uint8]
        return QStatus(self.__lib.alljoyn_busattachment_enablepeersecurity(bus, authMechanisms, listener, keyStoreFileName, isShared)) 


    # wrapper for alljoyn_busattachment_ispeersecurityenabled returns QCC_BOOL
    def BusattachmentIspeersecurityenabled(self, bus):  # alljoyn_busattachment
        self.__lib.alljoyn_busattachment_ispeersecurityenabled.restype = C.c_uint
        self.__lib.alljoyn_busattachment_ispeersecurityenabled.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_busattachment_ispeersecurityenabled(bus) 


    # wrapper for alljoyn_busattachment_createinterfacesfromxml returns QStatus
    def BusattachmentCreateinterfacesfromxml(self, bus, xml):  # alljoyn_busattachment, const char *
        self.__lib.alljoyn_busattachment_createinterfacesfromxml.restype = C.c_uint
        self.__lib.alljoyn_busattachment_createinterfacesfromxml.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_busattachment_createinterfacesfromxml(bus, xml)) 


    # wrapper for alljoyn_busattachment_deleteinterface returns QStatus
    def BusattachmentDeleteinterface(self, bus, iface):  # alljoyn_busattachment, alljoyn_interfacedescription
        self.__lib.alljoyn_busattachment_deleteinterface.restype = C.c_uint
        self.__lib.alljoyn_busattachment_deleteinterface.argtypes = [C.c_void_p, C.c_void_p]
        return QStatus(self.__lib.alljoyn_busattachment_deleteinterface(bus, iface)) 


    # wrapper for alljoyn_busattachment_isstarted returns QCC_BOOL
    def BusattachmentIsstarted(self, bus):  # alljoyn_busattachment
        self.__lib.alljoyn_busattachment_isstarted.restype = C.c_uint
        self.__lib.alljoyn_busattachment_isstarted.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_busattachment_isstarted(bus) 


    # wrapper for alljoyn_busattachment_isstopping returns QCC_BOOL
    def BusattachmentIsstopping(self, bus):  # alljoyn_busattachment
        self.__lib.alljoyn_busattachment_isstopping.restype = C.c_uint
        self.__lib.alljoyn_busattachment_isstopping.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_busattachment_isstopping(bus) 


    # wrapper for alljoyn_busattachment_isconnected returns QCC_BOOL
    def BusattachmentIsconnected(self, bus):  # const alljoyn_busattachment
        self.__lib.alljoyn_busattachment_isconnected.restype = C.c_uint
        self.__lib.alljoyn_busattachment_isconnected.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_busattachment_isconnected(bus) 


    # wrapper for alljoyn_busattachment_disconnect returns QStatus
    def BusattachmentDisconnect(self, bus, unused):  # alljoyn_busattachment, const char *
        self.__lib.alljoyn_busattachment_disconnect.restype = C.c_uint
        self.__lib.alljoyn_busattachment_disconnect.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_busattachment_disconnect(bus, unused)) 


    # wrapper for alljoyn_busattachment_getdbusproxyobj returns const alljoyn_proxybusobject
    def BusattachmentGetdbusproxyobj(self, bus):  # alljoyn_busattachment
        self.__lib.alljoyn_busattachment_getdbusproxyobj.restype = C.c_void_p
        self.__lib.alljoyn_busattachment_getdbusproxyobj.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_busattachment_getdbusproxyobj(bus) 


    # wrapper for alljoyn_busattachment_getalljoynproxyobj returns const alljoyn_proxybusobject
    def BusattachmentGetalljoynproxyobj(self, bus):  # alljoyn_busattachment
        self.__lib.alljoyn_busattachment_getalljoynproxyobj.restype = C.c_void_p
        self.__lib.alljoyn_busattachment_getalljoynproxyobj.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_busattachment_getalljoynproxyobj(bus) 


    # wrapper for alljoyn_busattachment_getalljoyndebugobj returns const alljoyn_proxybusobject
    def BusattachmentGetalljoyndebugobj(self, bus):  # alljoyn_busattachment
        self.__lib.alljoyn_busattachment_getalljoyndebugobj.restype = C.c_void_p
        self.__lib.alljoyn_busattachment_getalljoyndebugobj.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_busattachment_getalljoyndebugobj(bus) 


    # wrapper for alljoyn_busattachment_getuniquename returns const char *
    def BusattachmentGetuniquename(self, bus):  # const alljoyn_busattachment
        self.__lib.alljoyn_busattachment_getuniquename.restype = C.c_char_p
        self.__lib.alljoyn_busattachment_getuniquename.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_busattachment_getuniquename(bus) 


    # wrapper for alljoyn_busattachment_getglobalguidstring returns const char *
    def BusattachmentGetglobalguidstring(self, bus):  # const alljoyn_busattachment
        self.__lib.alljoyn_busattachment_getglobalguidstring.restype = C.c_char_p
        self.__lib.alljoyn_busattachment_getglobalguidstring.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_busattachment_getglobalguidstring(bus) 


    # wrapper for alljoyn_busattachment_unregisterallhandlers returns QStatus
    def BusattachmentUnregisterallhandlers(self, bus):  # alljoyn_busattachment
        self.__lib.alljoyn_busattachment_unregisterallhandlers.restype = C.c_uint
        self.__lib.alljoyn_busattachment_unregisterallhandlers.argtypes = [C.c_void_p]
        return QStatus(self.__lib.alljoyn_busattachment_unregisterallhandlers(bus)) 


    # wrapper for alljoyn_busattachment_registerkeystorelistener returns QStatus
    def BusattachmentRegisterkeystorelistener(self, bus, listener):  # alljoyn_busattachment, alljoyn_keystorelistener
        self.__lib.alljoyn_busattachment_registerkeystorelistener.restype = C.c_uint
        self.__lib.alljoyn_busattachment_registerkeystorelistener.argtypes = [C.c_void_p, C.c_void_p]
        return QStatus(self.__lib.alljoyn_busattachment_registerkeystorelistener(bus, listener)) 


    # wrapper for alljoyn_busattachment_reloadkeystore returns QStatus
    def BusattachmentReloadkeystore(self, bus):  # alljoyn_busattachment
        self.__lib.alljoyn_busattachment_reloadkeystore.restype = C.c_uint
        self.__lib.alljoyn_busattachment_reloadkeystore.argtypes = [C.c_void_p]
        return QStatus(self.__lib.alljoyn_busattachment_reloadkeystore(bus)) 


    # wrapper for alljoyn_busattachment_clearkeystore returns void
    def BusattachmentClearkeystore(self, bus):  # alljoyn_busattachment
        self.__lib.alljoyn_busattachment_clearkeystore.argtypes = [C.c_void_p]
        self.__lib.alljoyn_busattachment_clearkeystore(bus) 


    # wrapper for alljoyn_busattachment_clearkeys returns QStatus
    def BusattachmentClearkeys(self, bus, guid):  # alljoyn_busattachment, const char *
        self.__lib.alljoyn_busattachment_clearkeys.restype = C.c_uint
        self.__lib.alljoyn_busattachment_clearkeys.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_busattachment_clearkeys(bus, guid)) 


    # wrapper for alljoyn_busattachment_setkeyexpiration returns QStatus
    def BusattachmentSetkeyexpiration(self, bus, guid, timeout):  # alljoyn_busattachment, const char *, uint32_t
        self.__lib.alljoyn_busattachment_setkeyexpiration.restype = C.c_uint
        self.__lib.alljoyn_busattachment_setkeyexpiration.argtypes = [C.c_void_p, C.c_char_p, C.uint32_t]
        return QStatus(self.__lib.alljoyn_busattachment_setkeyexpiration(bus, guid, timeout)) 


    # wrapper for alljoyn_busattachment_getkeyexpiration returns QStatus
    def BusattachmentGetkeyexpiration(self, bus, guid, timeout):  # alljoyn_busattachment, const char *, uint32_t *
        self.__lib.alljoyn_busattachment_getkeyexpiration.restype = C.c_uint
        self.__lib.alljoyn_busattachment_getkeyexpiration.argtypes = [C.c_void_p, C.c_char_p, POINTER(C.c_uint32)]
        return QStatus(self.__lib.alljoyn_busattachment_getkeyexpiration(bus, guid, timeout)) 


    # wrapper for alljoyn_busattachment_addlogonentry returns QStatus
    def BusattachmentAddlogonentry(self, bus, authMechanism, userName, password):  # alljoyn_busattachment, const char *, const char *, const char *
        self.__lib.alljoyn_busattachment_addlogonentry.restype = C.c_uint
        self.__lib.alljoyn_busattachment_addlogonentry.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_busattachment_addlogonentry(bus, authMechanism, userName, password)) 


    # wrapper for alljoyn_busattachment_addmatch returns QStatus
    def BusattachmentAddmatch(self, bus, rule):  # alljoyn_busattachment, const char *
        self.__lib.alljoyn_busattachment_addmatch.restype = C.c_uint
        self.__lib.alljoyn_busattachment_addmatch.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_busattachment_addmatch(bus, rule)) 


    # wrapper for alljoyn_busattachment_removematch returns QStatus
    def BusattachmentRemovematch(self, bus, rule):  # alljoyn_busattachment, const char *
        self.__lib.alljoyn_busattachment_removematch.restype = C.c_uint
        self.__lib.alljoyn_busattachment_removematch.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_busattachment_removematch(bus, rule)) 


    # wrapper for alljoyn_busattachment_setsessionlistener returns QStatus
    def BusattachmentSetsessionlistener(self, bus, sessionId, listener):  # alljoyn_busattachment, alljoyn_sessionid, alljoyn_sessionlistener
        self.__lib.alljoyn_busattachment_setsessionlistener.restype = C.c_uint
        self.__lib.alljoyn_busattachment_setsessionlistener.argtypes = [C.c_void_p, C.c_uint32, C.c_void_p]
        return QStatus(self.__lib.alljoyn_busattachment_setsessionlistener(bus, sessionId, listener)) 


    # wrapper for alljoyn_busattachment_leavesession returns QStatus
    def BusattachmentLeavesession(self, bus, sessionId):  # alljoyn_busattachment, alljoyn_sessionid
        self.__lib.alljoyn_busattachment_leavesession.restype = C.c_uint
        self.__lib.alljoyn_busattachment_leavesession.argtypes = [C.c_void_p, C.c_uint32]
        return QStatus(self.__lib.alljoyn_busattachment_leavesession(bus, sessionId)) 


    # wrapper for alljoyn_busattachment_secureconnection returns QStatus
    def BusattachmentSecureconnection(self, bus, name, forceAuth):  # alljoyn_busattachment, const char *, QCC_BOOL
        self.__lib.alljoyn_busattachment_secureconnection.restype = C.c_uint
        self.__lib.alljoyn_busattachment_secureconnection.argtypes = [C.c_void_p, C.c_char_p, C.c_uint8]
        return QStatus(self.__lib.alljoyn_busattachment_secureconnection(bus, name, forceAuth)) 


    # wrapper for alljoyn_busattachment_secureconnectionasync returns QStatus
    def BusattachmentSecureconnectionasync(self, bus, name, forceAuth):  # alljoyn_busattachment, const char *, QCC_BOOL
        self.__lib.alljoyn_busattachment_secureconnectionasync.restype = C.c_uint
        self.__lib.alljoyn_busattachment_secureconnectionasync.argtypes = [C.c_void_p, C.c_char_p, C.c_uint8]
        return QStatus(self.__lib.alljoyn_busattachment_secureconnectionasync(bus, name, forceAuth)) 


    # wrapper for alljoyn_busattachment_removesessionmember returns QStatus
    def BusattachmentRemovesessionmember(self, bus, sessionId, memberName):  # alljoyn_busattachment, alljoyn_sessionid, const char *
        self.__lib.alljoyn_busattachment_removesessionmember.restype = C.c_uint
        self.__lib.alljoyn_busattachment_removesessionmember.argtypes = [C.c_void_p, C.c_uint32, C.c_char_p]
        return QStatus(self.__lib.alljoyn_busattachment_removesessionmember(bus, sessionId, memberName)) 


    # wrapper for alljoyn_busattachment_setlinktimeout returns QStatus
    def BusattachmentSetlinktimeout(self, bus, sessionid, linkTimeout):  # alljoyn_busattachment, alljoyn_sessionid, uint32_t *
        self.__lib.alljoyn_busattachment_setlinktimeout.restype = C.c_uint
        self.__lib.alljoyn_busattachment_setlinktimeout.argtypes = [C.c_void_p, C.c_uint32, POINTER(C.c_uint32)]
        return QStatus(self.__lib.alljoyn_busattachment_setlinktimeout(bus, sessionid, linkTimeout)) 


    # wrapper for alljoyn_busattachment_namehasowner returns QStatus
    def BusattachmentNamehasowner(self, bus, name, hasOwner):  # alljoyn_busattachment, const char *, QCC_BOOL *
        self.__lib.alljoyn_busattachment_namehasowner.restype = C.c_uint
        self.__lib.alljoyn_busattachment_namehasowner.argtypes = [C.c_void_p, C.c_char_p, POINTER(C.c_uint8)]
        return QStatus(self.__lib.alljoyn_busattachment_namehasowner(bus, name, hasOwner)) 


    # wrapper for alljoyn_busattachment_getpeerguid returns QStatus
    def BusattachmentGetpeerguid(self, bus, name, guid, guidSz):  # alljoyn_busattachment, const char *, char *, size_t *
        self.__lib.alljoyn_busattachment_getpeerguid.restype = C.c_uint
        self.__lib.alljoyn_busattachment_getpeerguid.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p, POINTER(C.csize_t)]
        return QStatus(self.__lib.alljoyn_busattachment_getpeerguid(bus, name, guid, guidSz)) 


    # wrapper for alljoyn_busattachment_setdaemondebug returns QStatus
    def BusattachmentSetdaemondebug(self, bus, module, level):  # alljoyn_busattachment, const char *, uint32_t
        self.__lib.alljoyn_busattachment_setdaemondebug.restype = C.c_uint
        self.__lib.alljoyn_busattachment_setdaemondebug.argtypes = [C.c_void_p, C.c_char_p, C.uint32_t]
        return QStatus(self.__lib.alljoyn_busattachment_setdaemondebug(bus, module, level)) 


    # wrapper for alljoyn_busattachment_ping returns QStatus
    def BusattachmentPing(self, bus, name, timeout):  # alljoyn_busattachment, const char *, uint32_t
        self.__lib.alljoyn_busattachment_ping.restype = C.c_uint
        self.__lib.alljoyn_busattachment_ping.argtypes = [C.c_void_p, C.c_char_p, C.uint32_t]
        return QStatus(self.__lib.alljoyn_busattachment_ping(bus, name, timeout)) 


    # wrapper for alljoyn_busattachment_registeraboutlistener returns void
    def BusattachmentRegisteraboutlistener(self, bus, aboutListener):  # alljoyn_busattachment, alljoyn_aboutlistener
        self.__lib.alljoyn_busattachment_registeraboutlistener.argtypes = [C.c_void_p, C.c_void_p]
        self.__lib.alljoyn_busattachment_registeraboutlistener(bus, aboutListener) 


    # wrapper for alljoyn_busattachment_unregisteraboutlistener returns void
    def BusattachmentUnregisteraboutlistener(self, bus, aboutListener):  # alljoyn_busattachment, alljoyn_aboutlistener
        self.__lib.alljoyn_busattachment_unregisteraboutlistener.argtypes = [C.c_void_p, C.c_void_p]
        self.__lib.alljoyn_busattachment_unregisteraboutlistener(bus, aboutListener) 


    # wrapper for alljoyn_busattachment_unregisterallaboutlisteners returns void
    def BusattachmentUnregisterallaboutlisteners(self, bus):  # alljoyn_busattachment
        self.__lib.alljoyn_busattachment_unregisterallaboutlisteners.argtypes = [C.c_void_p]
        self.__lib.alljoyn_busattachment_unregisterallaboutlisteners(bus) 


    # wrapper for alljoyn_busattachment_whoimplements_interfaces returns QStatus
    def BusattachmentWhoimplementsInterfaces(self, bus, implementsInterfaces, numberInterfaces):  # alljoyn_busattachment, const char * *, size_t
        self.__lib.alljoyn_busattachment_whoimplements_interfaces.restype = C.c_uint
        self.__lib.alljoyn_busattachment_whoimplements_interfaces.argtypes = [C.c_void_p, POINTER(C.c_char_p), C.csize_t]
        return QStatus(self.__lib.alljoyn_busattachment_whoimplements_interfaces(bus, implementsInterfaces, numberInterfaces)) 


    # wrapper for alljoyn_busattachment_whoimplements_interface returns QStatus
    def BusattachmentWhoimplementsInterface(self, bus, implementsInterface):  # alljoyn_busattachment, const char *
        self.__lib.alljoyn_busattachment_whoimplements_interface.restype = C.c_uint
        self.__lib.alljoyn_busattachment_whoimplements_interface.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_busattachment_whoimplements_interface(bus, implementsInterface)) 


    # wrapper for alljoyn_busattachment_cancelwhoimplements_interfaces returns QStatus
    def BusattachmentCancelwhoimplementsInterfaces(self, bus, implementsInterfaces, numberInterfaces):  # alljoyn_busattachment, const char * *, size_t
        self.__lib.alljoyn_busattachment_cancelwhoimplements_interfaces.restype = C.c_uint
        self.__lib.alljoyn_busattachment_cancelwhoimplements_interfaces.argtypes = [C.c_void_p, POINTER(C.c_char_p), C.csize_t]
        return QStatus(self.__lib.alljoyn_busattachment_cancelwhoimplements_interfaces(bus, implementsInterfaces, numberInterfaces)) 


    # wrapper for alljoyn_busattachment_cancelwhoimplements_interface returns QStatus
    def BusattachmentCancelwhoimplementsInterface(self, bus, implementsInterface):  # alljoyn_busattachment, const char *
        self.__lib.alljoyn_busattachment_cancelwhoimplements_interface.restype = C.c_uint
        self.__lib.alljoyn_busattachment_cancelwhoimplements_interface.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_busattachment_cancelwhoimplements_interface(bus, implementsInterface)) 


class AuthListener(object):
    
    __metaclass__ = AllJoynMeta
    
    def __init__(self, callbacks, context):
        self.handle = self.AboutlistenerCreate(callbacks, context)
    
    def __del__(self):
        self.AboutlistenerDestroy(self.handle)
        
    # wrapper for alljoyn_aboutlistener_create returns alljoyn_aboutlistener
    def AboutlistenerCreate(self, callbacks, context): 
        self.__lib.alljoyn_aboutlistener_create.restype = C.c_void_p
        self.__lib.alljoyn_aboutlistener_create.argtypes = [POINTER(AboutListenerCallback), C.c_void_p]  # const alljoyn_aboutlistener_callback* callback ,const void* context
        return self.__lib.alljoyn_aboutlistener_create(callbacks, context) 
        
    alljoyn_aboutlistener  alljoyn_aboutlistener_create();
    
    # wrapper for alljoyn_aboutlistener_destroy returns void
    def AboutlistenerDestroy(self, listener):  # alljoyn_aboutlistener
        self.__lib.alljoyn_aboutlistener_destroy.argtypes = [C.c_void_p]
        self.__lib.alljoyn_aboutlistener_destroy(listener) 


class Message(object):
    
    __metaclass__ = AllJoynMeta
    
    def __init__(self, bus):
        self.handle = self.MessageCreate(bus)
    
    def __del__(self):
        self.MessageDestroy(self.handle)
        
        # wrapper for alljoyn_message_create returns alljoyn_message
    def MessageCreate(self, bus):  # alljoyn_busattachment
        self.__lib.alljoyn_message_create.restype = C.c_void_p
        self.__lib.alljoyn_message_create.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_message_create(bus) 


    # wrapper for alljoyn_message_destroy returns void
    def MessageDestroy(self, msg):  # alljoyn_message
        self.__lib.alljoyn_message_destroy.argtypes = [C.c_void_p]
        self.__lib.alljoyn_message_destroy(msg) 


    # wrapper for alljoyn_message_isbroadcastsignal returns QCC_BOOL
    def MessageIsbroadcastsignal(self, msg):  # alljoyn_message
        self.__lib.alljoyn_message_isbroadcastsignal.restype = C.c_uint
        self.__lib.alljoyn_message_isbroadcastsignal.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_message_isbroadcastsignal(msg) 


    # wrapper for alljoyn_message_isglobalbroadcast returns QCC_BOOL
    def MessageIsglobalbroadcast(self, msg):  # alljoyn_message
        self.__lib.alljoyn_message_isglobalbroadcast.restype = C.c_uint
        self.__lib.alljoyn_message_isglobalbroadcast.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_message_isglobalbroadcast(msg) 


    # wrapper for alljoyn_message_issessionless returns QCC_BOOL
    def MessageIssessionless(self, msg):  # alljoyn_message
        self.__lib.alljoyn_message_issessionless.restype = C.c_uint
        self.__lib.alljoyn_message_issessionless.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_message_issessionless(msg) 


    # wrapper for alljoyn_message_getflags returns uint8_t
    def MessageGetflags(self, msg):  # alljoyn_message
        self.__lib.alljoyn_message_getflags.restype = C.c_uint8
        self.__lib.alljoyn_message_getflags.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_message_getflags(msg) 


    # wrapper for alljoyn_message_isexpired returns QCC_BOOL
    def MessageIsexpired(self, msg, tillExpireMS):  # alljoyn_message, uint32_t *
        self.__lib.alljoyn_message_isexpired.restype = C.c_uint
        self.__lib.alljoyn_message_isexpired.argtypes = [C.c_void_p, POINTER(C.c_uint32)]
        return self.__lib.alljoyn_message_isexpired(msg, tillExpireMS) 


    # wrapper for alljoyn_message_isunreliable returns QCC_BOOL
    def MessageIsunreliable(self, msg):  # alljoyn_message
        self.__lib.alljoyn_message_isunreliable.restype = C.c_uint
        self.__lib.alljoyn_message_isunreliable.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_message_isunreliable(msg) 


    # wrapper for alljoyn_message_isencrypted returns QCC_BOOL
    def MessageIsencrypted(self, msg):  # alljoyn_message
        self.__lib.alljoyn_message_isencrypted.restype = C.c_uint
        self.__lib.alljoyn_message_isencrypted.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_message_isencrypted(msg) 


    # wrapper for alljoyn_message_getauthmechanism returns const char *
    def MessageGetauthmechanism(self, msg):  # alljoyn_message
        self.__lib.alljoyn_message_getauthmechanism.restype = C.c_char_p
        self.__lib.alljoyn_message_getauthmechanism.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_message_getauthmechanism(msg) 


    # wrapper for alljoyn_message_gettype returns alljoyn_messagetype
    def MessageGettype(self, msg):  # alljoyn_message
        self.__lib.alljoyn_message_gettype.restype = C.c_uint32
        self.__lib.alljoyn_message_gettype.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_message_gettype(msg) 


    # wrapper for alljoyn_message_parseargs returns QStatus
    def MessageParseargs(self, msg, signature):  # alljoyn_message, const char *
        self.__lib.alljoyn_message_parseargs.restype = C.c_uint
        self.__lib.alljoyn_message_parseargs.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_message_parseargs(msg, signature)) 


    # wrapper for alljoyn_message_getcallserial returns uint32_t
    def MessageGetcallserial(self, msg):  # alljoyn_message
        self.__lib.alljoyn_message_getcallserial.restype = C.c_uint32
        self.__lib.alljoyn_message_getcallserial.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_message_getcallserial(msg) 


    # wrapper for alljoyn_message_getsignature returns const char *
    def MessageGetsignature(self, msg):  # alljoyn_message
        self.__lib.alljoyn_message_getsignature.restype = C.c_char_p
        self.__lib.alljoyn_message_getsignature.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_message_getsignature(msg) 


    # wrapper for alljoyn_message_getobjectpath returns const char *
    def MessageGetobjectpath(self, msg):  # alljoyn_message
        self.__lib.alljoyn_message_getobjectpath.restype = C.c_char_p
        self.__lib.alljoyn_message_getobjectpath.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_message_getobjectpath(msg) 


    # wrapper for alljoyn_message_getinterface returns const char *
    def MessageGetinterface(self, msg):  # alljoyn_message
        self.__lib.alljoyn_message_getinterface.restype = C.c_char_p
        self.__lib.alljoyn_message_getinterface.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_message_getinterface(msg) 


    # wrapper for alljoyn_message_getmembername returns const char *
    def MessageGetmembername(self, msg):  # alljoyn_message
        self.__lib.alljoyn_message_getmembername.restype = C.c_char_p
        self.__lib.alljoyn_message_getmembername.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_message_getmembername(msg) 


    # wrapper for alljoyn_message_getreplyserial returns uint32_t
    def MessageGetreplyserial(self, msg):  # alljoyn_message
        self.__lib.alljoyn_message_getreplyserial.restype = C.c_uint32
        self.__lib.alljoyn_message_getreplyserial.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_message_getreplyserial(msg) 


    # wrapper for alljoyn_message_getsender returns const char *
    def MessageGetsender(self, msg):  # alljoyn_message
        self.__lib.alljoyn_message_getsender.restype = C.c_char_p
        self.__lib.alljoyn_message_getsender.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_message_getsender(msg) 


    # wrapper for alljoyn_message_getreceiveendpointname returns const char *
    def MessageGetreceiveendpointname(self, msg):  # alljoyn_message
        self.__lib.alljoyn_message_getreceiveendpointname.restype = C.c_char_p
        self.__lib.alljoyn_message_getreceiveendpointname.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_message_getreceiveendpointname(msg) 


    # wrapper for alljoyn_message_getdestination returns const char *
    def MessageGetdestination(self, msg):  # alljoyn_message
        self.__lib.alljoyn_message_getdestination.restype = C.c_char_p
        self.__lib.alljoyn_message_getdestination.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_message_getdestination(msg) 


    # wrapper for alljoyn_message_getsessionid returns alljoyn_sessionid
    def MessageGetsessionid(self, msg):  # alljoyn_message
        self.__lib.alljoyn_message_getsessionid.restype = C.c_uint32
        self.__lib.alljoyn_message_getsessionid.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_message_getsessionid(msg) 


    # wrapper for alljoyn_message_geterrorname returns const char *
    def MessageGeterrorname(self, msg, errorMessage, errorMessage_size):  # alljoyn_message, char *, size_t *
        self.__lib.alljoyn_message_geterrorname.restype = C.c_char_p
        self.__lib.alljoyn_message_geterrorname.argtypes = [C.c_void_p, C.c_char_p, POINTER(C.csize_t)]
        return self.__lib.alljoyn_message_geterrorname(msg, errorMessage, errorMessage_size) 


    # wrapper for alljoyn_message_tostring returns size_t
    def MessageTostring(self, msg, str, buf):  # alljoyn_message, char *, size_t
        self.__lib.alljoyn_message_tostring.restype = C.c_size_t
        self.__lib.alljoyn_message_tostring.argtypes = [C.c_void_p, C.c_char_p, C.csize_t]
        return self.__lib.alljoyn_message_tostring(msg, str, buf) 


    # wrapper for alljoyn_message_description returns size_t
    def MessageDescription(self, msg, str, buf):  # alljoyn_message, char *, size_t
        self.__lib.alljoyn_message_description.restype = C.c_size_t
        self.__lib.alljoyn_message_description.argtypes = [C.c_void_p, C.c_char_p, C.csize_t]
        return self.__lib.alljoyn_message_description(msg, str, buf) 


    # wrapper for alljoyn_message_gettimestamp returns uint32_t
    def MessageGettimestamp(self, msg):  # alljoyn_message
        self.__lib.alljoyn_message_gettimestamp.restype = C.c_uint32
        self.__lib.alljoyn_message_gettimestamp.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_message_gettimestamp(msg) 


    # wrapper for alljoyn_message_setendianess returns void
    def MessageSetendianess(self, endian):  # const char
        self.__lib.alljoyn_message_setendianess.argtypes = [C.c_int8]
        self.__lib.alljoyn_message_setendianess(endian) 



class MsgArg(object):
    
    __metaclass__ = AllJoynMeta
    
    def __init__(self, bus):
        self.handle = self.MessageCreate(bus)
    
    def __del__(self):
        self.MessageDestroy(self.handle)
        
    def Signature(self, str_buf, buf):
        return self.MsgargSignature(self.handle, str_buf, buf)
        
    def GetString(self, s):
        return self.MsgargGetString(self.handle, s)
        
    # wrapper for alljoyn_msgarg_create returns C.c_void_p
    def MsgArgCreate(self):  # alljoyn_msgarg_create
        self.__lib.alljoyn_interfacedescription_addmember.restype = C.c_void_p
        return C.c_type_p(self.__lib.alljoyn_msgarg_create()

    # wrapper for alljoyn_msgarg_create_and_set returns alljoyn_msgarg
    def MsgargCreateAndSet(self, signature):  # const char *
        self.__lib.alljoyn_msgarg_create_and_set.restype = C.c_void_p
        self.__lib.alljoyn_msgarg_create_and_set.argtypes = [C.c_char_p]
        return self.__lib.alljoyn_msgarg_create_and_set(signature) 


    # wrapper for alljoyn_msgarg_destroy returns void
    def MsgargDestroy(self, arg):  # alljoyn_msgarg
        self.__lib.alljoyn_msgarg_destroy.argtypes = [C.c_void_p]
        self.__lib.alljoyn_msgarg_destroy(arg) 


    # wrapper for alljoyn_msgarg_array_create returns alljoyn_msgarg
    def MsgargArrayCreate(self, size):  # size_t
        self.__lib.alljoyn_msgarg_array_create.restype = C.c_void_p
        self.__lib.alljoyn_msgarg_array_create.argtypes = [C.csize_t]
        return self.__lib.alljoyn_msgarg_array_create(size) 


    # wrapper for alljoyn_msgarg_array_element returns alljoyn_msgarg
    def MsgargArrayElement(self, arg, index):  # alljoyn_msgarg, size_t
        self.__lib.alljoyn_msgarg_array_element.restype = C.c_void_p
        self.__lib.alljoyn_msgarg_array_element.argtypes = [C.c_void_p, C.csize_t]
        return self.__lib.alljoyn_msgarg_array_element(arg, index) 


    # vaargs not supported by ctypes
    ## wrapper for alljoyn_msgarg_set returns QStatus
    #def MsgargSet(self, arg, signature):  # alljoyn_msgarg, const char *
    #    self.__lib.alljoyn_msgarg_set.restype = C.c_uint
    #    self.__lib.alljoyn_msgarg_set.argtypes = [C.c_void_p, C.c_char_p]
    #    return QStatus(self.__lib.alljoyn_msgarg_set(arg, signature)) 


    # vaargs not supported by ctypes
    # wrapper for alljoyn_msgarg_get returns QStatus
    #def MsgargGet(self, arg, signature):  # alljoyn_msgarg, const char *
    #    self.__lib.alljoyn_msgarg_get.restype = C.c_uint
    #    self.__lib.alljoyn_msgarg_get.argtypes = [C.c_void_p, C.c_char_p]
    #    return QStatus(self.__lib.alljoyn_msgarg_get(arg, signature)) 


    # wrapper for alljoyn_msgarg_copy returns alljoyn_msgarg
    def MsgargCopy(self, source):  # const alljoyn_msgarg
        self.__lib.alljoyn_msgarg_copy.restype = C.c_void_p
        self.__lib.alljoyn_msgarg_copy.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_msgarg_copy(source) 


    # wrapper for alljoyn_msgarg_clone returns void
    def MsgargClone(self, destination, source):  # alljoyn_msgarg, const alljoyn_msgarg
        self.__lib.alljoyn_msgarg_clone.argtypes = [C.c_void_p, C.c_void_p]
        self.__lib.alljoyn_msgarg_clone(destination, source) 


    # wrapper for alljoyn_msgarg_equal returns QCC_BOOL
    def MsgargEqual(self, lhv, rhv):  # alljoyn_msgarg, alljoyn_msgarg
        self.__lib.alljoyn_msgarg_equal.restype = C.c_uint
        self.__lib.alljoyn_msgarg_equal.argtypes = [C.c_void_p, C.c_void_p]
        return self.__lib.alljoyn_msgarg_equal(lhv, rhv) 


    # wrapper for alljoyn_msgarg_array_set returns QStatus
    def MsgargArraySet(self, args, numArgs, signature):  # alljoyn_msgarg, size_t *, const char *
        self.__lib.alljoyn_msgarg_array_set.restype = C.c_uint
        self.__lib.alljoyn_msgarg_array_set.argtypes = [C.c_void_p, POINTER(C.csize_t), C.c_char_p]
        return QStatus(self.__lib.alljoyn_msgarg_array_set(args, numArgs, signature)) 


    # wrapper for alljoyn_msgarg_array_get returns QStatus
    def MsgargArrayGet(self, args, numArgs, signature):  # const alljoyn_msgarg, size_t, const char *
        self.__lib.alljoyn_msgarg_array_get.restype = C.c_uint
        self.__lib.alljoyn_msgarg_array_get.argtypes = [C.c_void_p, C.csize_t, C.c_char_p]
        return QStatus(self.__lib.alljoyn_msgarg_array_get(args, numArgs, signature)) 


    # wrapper for alljoyn_msgarg_tostring returns size_t
    def MsgargTostring(self, arg, str, buf, indent):  # alljoyn_msgarg, char *, size_t, size_t
        self.__lib.alljoyn_msgarg_tostring.restype = C.c_size_t
        self.__lib.alljoyn_msgarg_tostring.argtypes = [C.c_void_p, C.c_char_p, C.csize_t, C.csize_t]
        return self.__lib.alljoyn_msgarg_tostring(arg, str, buf, indent) 


    # wrapper for alljoyn_msgarg_array_tostring returns size_t
    def MsgargArrayTostring(self, args, numArgs, str, buf, indent):  # const alljoyn_msgarg, size_t, char *, size_t, size_t
        self.__lib.alljoyn_msgarg_array_tostring.restype = C.c_size_t
        self.__lib.alljoyn_msgarg_array_tostring.argtypes = [C.c_void_p, C.csize_t, C.c_char_p, C.csize_t, C.csize_t]
        return self.__lib.alljoyn_msgarg_array_tostring(args, numArgs, str, buf, indent) 


    # wrapper for alljoyn_msgarg_signature returns size_t
    def MsgargSignature(self, arg, str_buf, buf):  # alljoyn_msgarg, char *, size_t
        self.__lib.alljoyn_msgarg_signature.restype = C.c_size_t
        self.__lib.alljoyn_msgarg_signature.argtypes = [C.c_void_p, C.c_char_p, C.csize_t]
        return self.__lib.alljoyn_msgarg_signature(arg, str_buf, buf) 


    # wrapper for alljoyn_msgarg_array_signature returns size_t
    def MsgargArraySignature(self, values, numValues, str_buf, buf):  # alljoyn_msgarg, size_t, char *, size_t
        self.__lib.alljoyn_msgarg_array_signature.restype = C.c_size_t
        self.__lib.alljoyn_msgarg_array_signature.argtypes = [C.c_void_p, C.csize_t, C.c_char_p, C.csize_t]
        return self.__lib.alljoyn_msgarg_array_signature(values, numValues, str_buf, buf) 


    # wrapper for alljoyn_msgarg_hassignature returns QCC_BOOL
    def MsgargHassignature(self, arg, signature):  # alljoyn_msgarg, const char *
        self.__lib.alljoyn_msgarg_hassignature.restype = C.c_uint
        self.__lib.alljoyn_msgarg_hassignature.argtypes = [C.c_void_p, C.c_char_p]
        return self.__lib.alljoyn_msgarg_hassignature(arg, signature) 


    # wrapper for alljoyn_msgarg_getdictelement returns QStatus
    def MsgargGetdictelement(self, arg, elemSig):  # alljoyn_msgarg, const char *
        self.__lib.alljoyn_msgarg_getdictelement.restype = C.c_uint
        self.__lib.alljoyn_msgarg_getdictelement.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_msgarg_getdictelement(arg, elemSig)) 


    # wrapper for alljoyn_msgarg_gettype returns alljoyn_typeid
    def MsgargGettype(self, arg):  # alljoyn_msgarg
        self.__lib.alljoyn_msgarg_gettype.restype = C.c_int32
        self.__lib.alljoyn_msgarg_gettype.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_msgarg_gettype(arg) 


    # wrapper for alljoyn_msgarg_clear returns void
    def MsgargClear(self, arg):  # alljoyn_msgarg
        self.__lib.alljoyn_msgarg_clear.argtypes = [C.c_void_p]
        self.__lib.alljoyn_msgarg_clear(arg) 


    # wrapper for alljoyn_msgarg_stabilize returns void
    def MsgargStabilize(self, arg):  # alljoyn_msgarg
        self.__lib.alljoyn_msgarg_stabilize.argtypes = [C.c_void_p]
        self.__lib.alljoyn_msgarg_stabilize(arg) 


    # wrapper for alljoyn_msgarg_array_set_offset returns QStatus
    def MsgargArraySetOffset(self, args, argOffset, numArgs, signature):  # alljoyn_msgarg, size_t, size_t *, const char *
        self.__lib.alljoyn_msgarg_array_set_offset.restype = C.c_uint
        self.__lib.alljoyn_msgarg_array_set_offset.argtypes = [C.c_void_p, C.csize_t, POINTER(C.csize_t), C.c_char_p]
        return QStatus(self.__lib.alljoyn_msgarg_array_set_offset(args, argOffset, numArgs, signature)) 


    # wrapper for alljoyn_msgarg_set_and_stabilize returns QStatus
    def MsgargSetAndStabilize(self, arg, signature):  # alljoyn_msgarg, const char *
        self.__lib.alljoyn_msgarg_set_and_stabilize.restype = C.c_uint
        self.__lib.alljoyn_msgarg_set_and_stabilize.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_msgarg_set_and_stabilize(arg, signature)) 


    # wrapper for alljoyn_msgarg_set_uint8 returns QStatus
    def MsgargSetUint8(self, arg, y):  # alljoyn_msgarg, uint8_t
        self.__lib.alljoyn_msgarg_set_uint8.restype = C.c_uint
        self.__lib.alljoyn_msgarg_set_uint8.argtypes = [C.c_void_p, C.c_uint8]
        return QStatus(self.__lib.alljoyn_msgarg_set_uint8(arg, y)) 


    # wrapper for alljoyn_msgarg_set_bool returns QStatus
    def MsgargSetBool(self, arg, b):  # alljoyn_msgarg, QCC_BOOL
        self.__lib.alljoyn_msgarg_set_bool.restype = C.c_uint
        self.__lib.alljoyn_msgarg_set_bool.argtypes = [C.c_void_p, C.c_uint8]
        return QStatus(self.__lib.alljoyn_msgarg_set_bool(arg, b)) 


    # wrapper for alljoyn_msgarg_set_int16 returns QStatus
    def MsgargSetInt16(self, arg, n):  # alljoyn_msgarg, int16_t
        self.__lib.alljoyn_msgarg_set_int16.restype = C.c_uint
        self.__lib.alljoyn_msgarg_set_int16.argtypes = [C.c_void_p, C.c_int16]
        return QStatus(self.__lib.alljoyn_msgarg_set_int16(arg, n)) 


    # wrapper for alljoyn_msgarg_set_uint16 returns QStatus
    def MsgargSetUint16(self, arg, q):  # alljoyn_msgarg, uint16_t
        self.__lib.alljoyn_msgarg_set_uint16.restype = C.c_uint
        self.__lib.alljoyn_msgarg_set_uint16.argtypes = [C.c_void_p, C.c_uint16]
        return QStatus(self.__lib.alljoyn_msgarg_set_uint16(arg, q)) 


    # wrapper for alljoyn_msgarg_set_int32 returns QStatus
    def MsgargSetInt32(self, arg, i):  # alljoyn_msgarg, int32_t
        self.__lib.alljoyn_msgarg_set_int32.restype = C.c_uint
        self.__lib.alljoyn_msgarg_set_int32.argtypes = [C.c_void_p, C.c_int32]
        return QStatus(self.__lib.alljoyn_msgarg_set_int32(arg, i)) 


    # wrapper for alljoyn_msgarg_set_uint32 returns QStatus
    def MsgargSetUint32(self, arg, u):  # alljoyn_msgarg, uint32_t
        self.__lib.alljoyn_msgarg_set_uint32.restype = C.c_uint
        self.__lib.alljoyn_msgarg_set_uint32.argtypes = [C.c_void_p, C.uint32_t]
        return QStatus(self.__lib.alljoyn_msgarg_set_uint32(arg, u)) 


    # wrapper for alljoyn_msgarg_set_int64 returns QStatus
    def MsgargSetInt64(self, arg, x):  # alljoyn_msgarg, int64_t
        self.__lib.alljoyn_msgarg_set_int64.restype = C.c_uint
        self.__lib.alljoyn_msgarg_set_int64.argtypes = [C.c_void_p, C.c_int64]
        return QStatus(self.__lib.alljoyn_msgarg_set_int64(arg, x)) 


    # wrapper for alljoyn_msgarg_set_uint64 returns QStatus
    def MsgargSetUint64(self, arg, t):  # alljoyn_msgarg, uint64_t
        self.__lib.alljoyn_msgarg_set_uint64.restype = C.c_uint
        self.__lib.alljoyn_msgarg_set_uint64.argtypes = [C.c_void_p, C.c_uint64]
        return QStatus(self.__lib.alljoyn_msgarg_set_uint64(arg, t)) 


    # wrapper for alljoyn_msgarg_set_double returns QStatus
    def MsgargSetDouble(self, arg, d):  # alljoyn_msgarg, double
        self.__lib.alljoyn_msgarg_set_double.restype = C.c_uint
        self.__lib.alljoyn_msgarg_set_double.argtypes = [C.c_void_p, C.c_double]
        return QStatus(self.__lib.alljoyn_msgarg_set_double(arg, d)) 


    # wrapper for alljoyn_msgarg_set_string returns QStatus
    def MsgargSetString(self, arg, s):  # alljoyn_msgarg, const char *
        self.__lib.alljoyn_msgarg_set_string.restype = C.c_uint
        self.__lib.alljoyn_msgarg_set_string.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_msgarg_set_string(arg, s)) 


    # wrapper for alljoyn_msgarg_set_objectpath returns QStatus
    def MsgargSetObjectpath(self, arg, o):  # alljoyn_msgarg, const char *
        self.__lib.alljoyn_msgarg_set_objectpath.restype = C.c_uint
        self.__lib.alljoyn_msgarg_set_objectpath.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_msgarg_set_objectpath(arg, o)) 


    # wrapper for alljoyn_msgarg_set_signature returns QStatus
    def MsgargSetSignature(self, arg, g):  # alljoyn_msgarg, const char *
        self.__lib.alljoyn_msgarg_set_signature.restype = C.c_uint
        self.__lib.alljoyn_msgarg_set_signature.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_msgarg_set_signature(arg, g)) 


    # wrapper for alljoyn_msgarg_get_uint8 returns QStatus
    def MsgargGetUint8(self, arg, y):  # const alljoyn_msgarg, uint8_t *
        self.__lib.alljoyn_msgarg_get_uint8.restype = C.c_uint
        self.__lib.alljoyn_msgarg_get_uint8.argtypes = [C.c_void_p, POINTER(C.c_uint8_t)]
        return QStatus(self.__lib.alljoyn_msgarg_get_uint8(arg, y)) 


    # wrapper for alljoyn_msgarg_get_bool returns QStatus
    def MsgargGetBool(self, arg, b):  # const alljoyn_msgarg, QCC_BOOL *
        self.__lib.alljoyn_msgarg_get_bool.restype = C.c_uint
        self.__lib.alljoyn_msgarg_get_bool.argtypes = [C.c_void_p, POINTER(C.c_uint8)]
        return QStatus(self.__lib.alljoyn_msgarg_get_bool(arg, b)) 


    # wrapper for alljoyn_msgarg_get_int16 returns QStatus
    def MsgargGetInt16(self, arg, n):  # const alljoyn_msgarg, int16_t *
        self.__lib.alljoyn_msgarg_get_int16.restype = C.c_uint
        self.__lib.alljoyn_msgarg_get_int16.argtypes = [C.c_void_p, POINTER(C.c_int16)]
        return QStatus(self.__lib.alljoyn_msgarg_get_int16(arg, n)) 


    # wrapper for alljoyn_msgarg_get_uint16 returns QStatus
    def MsgargGetUint16(self, arg, q):  # const alljoyn_msgarg, uint16_t *
        self.__lib.alljoyn_msgarg_get_uint16.restype = C.c_uint
        self.__lib.alljoyn_msgarg_get_uint16.argtypes = [C.c_void_p, POINTER(C.c_uint16)]
        return QStatus(self.__lib.alljoyn_msgarg_get_uint16(arg, q)) 


    # wrapper for alljoyn_msgarg_get_int32 returns QStatus
    def MsgargGetInt32(self, arg, i):  # const alljoyn_msgarg, int32_t *
        self.__lib.alljoyn_msgarg_get_int32.restype = C.c_uint
        self.__lib.alljoyn_msgarg_get_int32.argtypes = [C.c_void_p, POINTER(C.c_int32)]
        return QStatus(self.__lib.alljoyn_msgarg_get_int32(arg, i)) 


    # wrapper for alljoyn_msgarg_get_uint32 returns QStatus
    def MsgargGetUint32(self, arg, u):  # const alljoyn_msgarg, uint32_t *
        self.__lib.alljoyn_msgarg_get_uint32.restype = C.c_uint
        self.__lib.alljoyn_msgarg_get_uint32.argtypes = [C.c_void_p, POINTER(C.c_uint32)]
        return QStatus(self.__lib.alljoyn_msgarg_get_uint32(arg, u)) 


    # wrapper for alljoyn_msgarg_get_int64 returns QStatus
    def MsgargGetInt64(self, arg, x):  # const alljoyn_msgarg, int64_t *
        self.__lib.alljoyn_msgarg_get_int64.restype = C.c_uint
        self.__lib.alljoyn_msgarg_get_int64.argtypes = [C.c_void_p, POINTER(C.c_int64)]
        return QStatus(self.__lib.alljoyn_msgarg_get_int64(arg, x)) 


    # wrapper for alljoyn_msgarg_get_uint64 returns QStatus
    def MsgargGetUint64(self, arg, t):  # const alljoyn_msgarg, uint64_t *
        self.__lib.alljoyn_msgarg_get_uint64.restype = C.c_uint
        self.__lib.alljoyn_msgarg_get_uint64.argtypes = [C.c_void_p, POINTER(C.c_uint64_t)]
        return QStatus(self.__lib.alljoyn_msgarg_get_uint64(arg, t)) 


    # wrapper for alljoyn_msgarg_get_double returns QStatus
    def MsgargGetDouble(self, arg, d):  # const alljoyn_msgarg, double *
        self.__lib.alljoyn_msgarg_get_double.restype = C.c_uint
        self.__lib.alljoyn_msgarg_get_double.argtypes = [C.c_void_p, POINTER(C.c_double)]
        return QStatus(self.__lib.alljoyn_msgarg_get_double(arg, d)) 


    # wrapper for alljoyn_msgarg_get_string returns QStatus
    def MsgargGetString(self, arg, s):  # const alljoyn_msgarg, char * *
        self.__lib.alljoyn_msgarg_get_string.restype = C.c_uint
        self.__lib.alljoyn_msgarg_get_string.argtypes = [C.c_void_p, POINTER(C.c_char_p)]
        return QStatus(self.__lib.alljoyn_msgarg_get_string(arg, s)) 


    # wrapper for alljoyn_msgarg_get_objectpath returns QStatus
    def MsgargGetObjectpath(self, arg, o):  # const alljoyn_msgarg, char * *
        self.__lib.alljoyn_msgarg_get_objectpath.restype = C.c_uint
        self.__lib.alljoyn_msgarg_get_objectpath.argtypes = [C.c_void_p, POINTER(C.c_char_p)]
        return QStatus(self.__lib.alljoyn_msgarg_get_objectpath(arg, o)) 


    # wrapper for alljoyn_msgarg_get_signature returns QStatus
    def MsgargGetSignature(self, arg, g):  # const alljoyn_msgarg, char * *
        self.__lib.alljoyn_msgarg_get_signature.restype = C.c_uint
        self.__lib.alljoyn_msgarg_get_signature.argtypes = [C.c_void_p, POINTER(C.c_char_p)]
        return QStatus(self.__lib.alljoyn_msgarg_get_signature(arg, g)) 


    # wrapper for alljoyn_msgarg_get_variant returns QStatus
    def MsgargGetVariant(self, arg, v):  # const alljoyn_msgarg, alljoyn_msgarg
        self.__lib.alljoyn_msgarg_get_variant.restype = C.c_uint
        self.__lib.alljoyn_msgarg_get_variant.argtypes = [C.c_void_p, C.c_void_p]
        return QStatus(self.__lib.alljoyn_msgarg_get_variant(arg, v)) 


    # wrapper for alljoyn_msgarg_set_uint8_array returns QStatus
    def MsgargSetUint8Array(self, arg, length, ay):  # alljoyn_msgarg, size_t, uint8_t *
        self.__lib.alljoyn_msgarg_set_uint8_array.restype = C.c_uint
        self.__lib.alljoyn_msgarg_set_uint8_array.argtypes = [C.c_void_p, C.csize_t, POINTER(C.c_uint8_t)]
        return QStatus(self.__lib.alljoyn_msgarg_set_uint8_array(arg, length, ay)) 


    # wrapper for alljoyn_msgarg_set_bool_array returns QStatus
    def MsgargSetBoolArray(self, arg, length, ab):  # alljoyn_msgarg, size_t, QCC_BOOL *
        self.__lib.alljoyn_msgarg_set_bool_array.restype = C.c_uint
        self.__lib.alljoyn_msgarg_set_bool_array.argtypes = [C.c_void_p, C.csize_t, POINTER(C.c_uint8)]
        return QStatus(self.__lib.alljoyn_msgarg_set_bool_array(arg, length, ab)) 


    # wrapper for alljoyn_msgarg_set_int16_array returns QStatus
    def MsgargSetInt16Array(self, arg, length, an):  # alljoyn_msgarg, size_t, int16_t *
        self.__lib.alljoyn_msgarg_set_int16_array.restype = C.c_uint
        self.__lib.alljoyn_msgarg_set_int16_array.argtypes = [C.c_void_p, C.csize_t, POINTER(C.c_int16)]
        return QStatus(self.__lib.alljoyn_msgarg_set_int16_array(arg, length, an)) 


    # wrapper for alljoyn_msgarg_set_uint16_array returns QStatus
    def MsgargSetUint16Array(self, arg, length, aq):  # alljoyn_msgarg, size_t, uint16_t *
        self.__lib.alljoyn_msgarg_set_uint16_array.restype = C.c_uint
        self.__lib.alljoyn_msgarg_set_uint16_array.argtypes = [C.c_void_p, C.csize_t, POINTER(C.c_uint16)]
        return QStatus(self.__lib.alljoyn_msgarg_set_uint16_array(arg, length, aq)) 


    # wrapper for alljoyn_msgarg_set_int32_array returns QStatus
    def MsgargSetInt32Array(self, arg, length, ai):  # alljoyn_msgarg, size_t, int32_t *
        self.__lib.alljoyn_msgarg_set_int32_array.restype = C.c_uint
        self.__lib.alljoyn_msgarg_set_int32_array.argtypes = [C.c_void_p, C.csize_t, POINTER(C.c_int32)]
        return QStatus(self.__lib.alljoyn_msgarg_set_int32_array(arg, length, ai)) 


    # wrapper for alljoyn_msgarg_set_uint32_array returns QStatus
    def MsgargSetUint32Array(self, arg, length, au):  # alljoyn_msgarg, size_t, uint32_t *
        self.__lib.alljoyn_msgarg_set_uint32_array.restype = C.c_uint
        self.__lib.alljoyn_msgarg_set_uint32_array.argtypes = [C.c_void_p, C.csize_t, POINTER(C.c_uint32)]
        return QStatus(self.__lib.alljoyn_msgarg_set_uint32_array(arg, length, au)) 


    # wrapper for alljoyn_msgarg_set_int64_array returns QStatus
    def MsgargSetInt64Array(self, arg, length, ax):  # alljoyn_msgarg, size_t, int64_t *
        self.__lib.alljoyn_msgarg_set_int64_array.restype = C.c_uint
        self.__lib.alljoyn_msgarg_set_int64_array.argtypes = [C.c_void_p, C.csize_t, POINTER(C.c_int64)]
        return QStatus(self.__lib.alljoyn_msgarg_set_int64_array(arg, length, ax)) 


    # wrapper for alljoyn_msgarg_set_uint64_array returns QStatus
    def MsgargSetUint64Array(self, arg, length, at):  # alljoyn_msgarg, size_t, uint64_t *
        self.__lib.alljoyn_msgarg_set_uint64_array.restype = C.c_uint
        self.__lib.alljoyn_msgarg_set_uint64_array.argtypes = [C.c_void_p, C.csize_t, POINTER(C.c_uint64_t)]
        return QStatus(self.__lib.alljoyn_msgarg_set_uint64_array(arg, length, at)) 


    # wrapper for alljoyn_msgarg_set_double_array returns QStatus
    def MsgargSetDoubleArray(self, arg, length, ad):  # alljoyn_msgarg, size_t, double *
        self.__lib.alljoyn_msgarg_set_double_array.restype = C.c_uint
        self.__lib.alljoyn_msgarg_set_double_array.argtypes = [C.c_void_p, C.csize_t, POINTER(C.c_double)]
        return QStatus(self.__lib.alljoyn_msgarg_set_double_array(arg, length, ad)) 


    # wrapper for alljoyn_msgarg_set_string_array returns QStatus
    def MsgargSetStringArray(self, arg, length, _as):  # alljoyn_msgarg, size_t, const char * *
        self.__lib.alljoyn_msgarg_set_string_array.restype = C.c_uint
        self.__lib.alljoyn_msgarg_set_string_array.argtypes = [C.c_void_p, C.csize_t, POINTER(C.c_char_p)]
        return QStatus(self.__lib.alljoyn_msgarg_set_string_array(arg, length, _as)) 


    # wrapper for alljoyn_msgarg_set_objectpath_array returns QStatus
    def MsgargSetObjectpathArray(self, arg, length, ao):  # alljoyn_msgarg, size_t, const char * *
        self.__lib.alljoyn_msgarg_set_objectpath_array.restype = C.c_uint
        self.__lib.alljoyn_msgarg_set_objectpath_array.argtypes = [C.c_void_p, C.csize_t, POINTER(C.c_char_p)]
        return QStatus(self.__lib.alljoyn_msgarg_set_objectpath_array(arg, length, ao)) 


    # wrapper for alljoyn_msgarg_set_signature_array returns QStatus
    def MsgargSetSignatureArray(self, arg, length, ag):  # alljoyn_msgarg, size_t, const char * *
        self.__lib.alljoyn_msgarg_set_signature_array.restype = C.c_uint
        self.__lib.alljoyn_msgarg_set_signature_array.argtypes = [C.c_void_p, C.csize_t, POINTER(C.c_char_p)]
        return QStatus(self.__lib.alljoyn_msgarg_set_signature_array(arg, length, ag)) 


    # wrapper for alljoyn_msgarg_get_uint8_array returns QStatus
    def MsgargGetUint8Array(self, arg, length, ay):  # const alljoyn_msgarg, size_t *, uint8_t *
        self.__lib.alljoyn_msgarg_get_uint8_array.restype = C.c_uint
        self.__lib.alljoyn_msgarg_get_uint8_array.argtypes = [C.c_void_p, POINTER(C.csize_t), POINTER(C.c_uint8_t)]
        return QStatus(self.__lib.alljoyn_msgarg_get_uint8_array(arg, length, ay)) 


    # wrapper for alljoyn_msgarg_get_bool_array returns QStatus
    def MsgargGetBoolArray(self, arg, length, ab):  # const alljoyn_msgarg, size_t *, QCC_BOOL *
        self.__lib.alljoyn_msgarg_get_bool_array.restype = C.c_uint
        self.__lib.alljoyn_msgarg_get_bool_array.argtypes = [C.c_void_p, POINTER(C.csize_t), POINTER(C.c_uint8)]
        return QStatus(self.__lib.alljoyn_msgarg_get_bool_array(arg, length, ab)) 


    # wrapper for alljoyn_msgarg_get_int16_array returns QStatus
    def MsgargGetInt16Array(self, arg, length, an):  # const alljoyn_msgarg, size_t *, int16_t *
        self.__lib.alljoyn_msgarg_get_int16_array.restype = C.c_uint
        self.__lib.alljoyn_msgarg_get_int16_array.argtypes = [C.c_void_p, POINTER(C.csize_t), POINTER(C.c_int16)]
        return QStatus(self.__lib.alljoyn_msgarg_get_int16_array(arg, length, an)) 


    # wrapper for alljoyn_msgarg_get_uint16_array returns QStatus
    def MsgargGetUint16Array(self, arg, length, aq):  # const alljoyn_msgarg, size_t *, uint16_t *
        self.__lib.alljoyn_msgarg_get_uint16_array.restype = C.c_uint
        self.__lib.alljoyn_msgarg_get_uint16_array.argtypes = [C.c_void_p, POINTER(C.csize_t), POINTER(C.c_uint16)]
        return QStatus(self.__lib.alljoyn_msgarg_get_uint16_array(arg, length, aq)) 


    # wrapper for alljoyn_msgarg_get_int32_array returns QStatus
    def MsgargGetInt32Array(self, arg, length, ai):  # const alljoyn_msgarg, size_t *, int32_t *
        self.__lib.alljoyn_msgarg_get_int32_array.restype = C.c_uint
        self.__lib.alljoyn_msgarg_get_int32_array.argtypes = [C.c_void_p, POINTER(C.csize_t), POINTER(C.c_int32)]
        return QStatus(self.__lib.alljoyn_msgarg_get_int32_array(arg, length, ai)) 


    # wrapper for alljoyn_msgarg_get_uint32_array returns QStatus
    def MsgargGetUint32Array(self, arg, length, au):  # const alljoyn_msgarg, size_t *, uint32_t *
        self.__lib.alljoyn_msgarg_get_uint32_array.restype = C.c_uint
        self.__lib.alljoyn_msgarg_get_uint32_array.argtypes = [C.c_void_p, POINTER(C.csize_t), POINTER(C.c_uint32)]
        return QStatus(self.__lib.alljoyn_msgarg_get_uint32_array(arg, length, au)) 


    # wrapper for alljoyn_msgarg_get_int64_array returns QStatus
    def MsgargGetInt64Array(self, arg, length, ax):  # const alljoyn_msgarg, size_t *, int64_t *
        self.__lib.alljoyn_msgarg_get_int64_array.restype = C.c_uint
        self.__lib.alljoyn_msgarg_get_int64_array.argtypes = [C.c_void_p, POINTER(C.csize_t), POINTER(C.c_int64)]
        return QStatus(self.__lib.alljoyn_msgarg_get_int64_array(arg, length, ax)) 


    # wrapper for alljoyn_msgarg_get_uint64_array returns QStatus
    def MsgargGetUint64Array(self, arg, length, at):  # const alljoyn_msgarg, size_t *, uint64_t *
        self.__lib.alljoyn_msgarg_get_uint64_array.restype = C.c_uint
        self.__lib.alljoyn_msgarg_get_uint64_array.argtypes = [C.c_void_p, POINTER(C.csize_t), POINTER(C.c_uint64_t)]
        return QStatus(self.__lib.alljoyn_msgarg_get_uint64_array(arg, length, at)) 


    # wrapper for alljoyn_msgarg_get_double_array returns QStatus
    def MsgargGetDoubleArray(self, arg, length, ad):  # const alljoyn_msgarg, size_t *, double *
        self.__lib.alljoyn_msgarg_get_double_array.restype = C.c_uint
        self.__lib.alljoyn_msgarg_get_double_array.argtypes = [C.c_void_p, POINTER(C.csize_t), POINTER(C.c_double)]
        return QStatus(self.__lib.alljoyn_msgarg_get_double_array(arg, length, ad)) 


    # wrapper for alljoyn_msgarg_get_array_numberofelements returns size_t
    def MsgargGetArrayNumberofelements(self, arg):  # const alljoyn_msgarg
        self.__lib.alljoyn_msgarg_get_array_numberofelements.restype = C.c_size_t
        self.__lib.alljoyn_msgarg_get_array_numberofelements.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_msgarg_get_array_numberofelements(arg) 


    # wrapper for alljoyn_msgarg_get_array_elementsignature returns const char *
    def MsgargGetArrayElementsignature(self, arg, index):  # const alljoyn_msgarg, size_t
        self.__lib.alljoyn_msgarg_get_array_elementsignature.restype = C.c_char_p
        self.__lib.alljoyn_msgarg_get_array_elementsignature.argtypes = [C.c_void_p, C.csize_t]
        return self.__lib.alljoyn_msgarg_get_array_elementsignature(arg, index) 


    # wrapper for alljoyn_msgarg_getkey returns alljoyn_msgarg
    def MsgargGetkey(self, arg):  # alljoyn_msgarg
        self.__lib.alljoyn_msgarg_getkey.restype = C.c_void_p
        self.__lib.alljoyn_msgarg_getkey.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_msgarg_getkey(arg) 


    # wrapper for alljoyn_msgarg_getvalue returns alljoyn_msgarg
    def MsgargGetvalue(self, arg):  # alljoyn_msgarg
        self.__lib.alljoyn_msgarg_getvalue.restype = C.c_void_p
        self.__lib.alljoyn_msgarg_getvalue.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_msgarg_getvalue(arg) 


    # wrapper for alljoyn_msgarg_setdictentry returns QStatus
    def MsgargSetdictentry(self, arg, key, value):  # alljoyn_msgarg, alljoyn_msgarg, alljoyn_msgarg
        self.__lib.alljoyn_msgarg_setdictentry.restype = C.c_uint
        self.__lib.alljoyn_msgarg_setdictentry.argtypes = [C.c_void_p, C.c_void_p, C.c_void_p]
        return QStatus(self.__lib.alljoyn_msgarg_setdictentry(arg, key, value)) 


    # wrapper for alljoyn_msgarg_setstruct returns QStatus
    def MsgargSetstruct(self, arg, struct_members, num_members):  # alljoyn_msgarg, alljoyn_msgarg, size_t
        self.__lib.alljoyn_msgarg_setstruct.restype = C.c_uint
        self.__lib.alljoyn_msgarg_setstruct.argtypes = [C.c_void_p, C.c_void_p, C.csize_t]
        return QStatus(self.__lib.alljoyn_msgarg_setstruct(arg, struct_members, num_members)) 


    # wrapper for alljoyn_msgarg_getnummembers returns size_t
    def MsgargGetnummembers(self, arg):  # alljoyn_msgarg
        self.__lib.alljoyn_msgarg_getnummembers.restype = C.c_size_t
        self.__lib.alljoyn_msgarg_getnummembers.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_msgarg_getnummembers(arg) 


    # wrapper for alljoyn_msgarg_getmember returns alljoyn_msgarg
    def MsgargGetmember(self, arg, index):  # alljoyn_msgarg, size_t
        self.__lib.alljoyn_msgarg_getmember.restype = C.c_void_p
        self.__lib.alljoyn_msgarg_getmember.argtypes = [C.c_void_p, C.csize_t]
        return self.__lib.alljoyn_msgarg_getmember(arg, index) 


class AllJoyn(object):
    
    def __init__(self, libraryName=None):
        """
        Init method for the class
        
        @param libraryName: library path, otherwise I'll look for it into the
                            standard path
        @type libraryName: string
        """
        
        # Used for test
        self.__num = 0
        # Used for test
        
        self.initCalled = 0
        self.__lib = library.internlLibrary(libraryName)


    ################ Attach callback functions #########################
    
    # wrapper for alljoyn_buslistener_create returns alljoyn_buslistener
    def BusListenerCreate(self, callbacks, context):
        self.__lib.alljoyn_buslistener_create.restype = C.c_void_p
        self.__lib.alljoyn_buslistener_create.argtypes = [POINTER(BusListenerCallbacks), C.c_void_p]
        return C.c_void_p(self.__lib.alljoyn_buslistener_create(callbacks, context))
            
    
    
    ##########################################


    
    
    def GetVersion(self):
        self.__lib.alljoyn_getversion.restype = C.c_char_p
        return self.__lib.alljoyn_getversion()

    def GetBuildInfo(self):
        self.__lib.alljoyn_getbuildinfo.restype = C.c_char_p
        return self.__lib.alljoyn_getbuildinfo()







    #############################################
    
    #QStatus  alljoyn_interfacedescription_addmember(alljoyn_interfacedescription iface, alljoyn_messagetype type ,const char* name, const char* inputSig, const char* outSig ,const char* argNames, uint8_t annotation);


    # wrapper for alljoyn_interfacedescription_addmember returns QStatus
    def InterfaceDescriptionAddMember(self, iface, type, name, inputSig, outSig, argNames, annotation):  # alljoyn_interfacedescription, alljoyn_messagetype, const char* name, const char* inputSig, const char* outSig ,const char* argNames, uint8_t annotation
        self.__lib.alljoyn_interfacedescription_addmember.restype = C.c_uint
        self.__lib.alljoyn_interfacedescription_addmember.argtypes = [C.c_void_p, C.c_uint32, C.c_char_p, C.c_char_p, C.c_char_p, C.c_char_p, C.c_uint8]
        return QStatus(self.__lib.alljoyn_interfacedescription_addmember(iface, type, name, inputSig, outSig, argNames, annotation))




    


   

    #############################################






















    










    # wrapper for alljoyn_unity_set_deferred_callback_mainthread_only returns void
    def UnitySetDeferredCallbackMainthreadOnly(self, mainthread_only):  # QCC_BOOL
        self.__lib.alljoyn_unity_set_deferred_callback_mainthread_only.argtypes = [C.c_uint8]
        self.__lib.alljoyn_unity_set_deferred_callback_mainthread_only(mainthread_only) 


    # wrapper for alljoyn_authlistener_requestcredentialsresponse returns QStatus
    def AuthlistenerRequestcredentialsresponse(self, listener, authContext, accept, credentials):  # alljoyn_authlistener, void *, QCC_BOOL, alljoyn_credentials
        self.__lib.alljoyn_authlistener_requestcredentialsresponse.restype = C.c_uint
        self.__lib.alljoyn_authlistener_requestcredentialsresponse.argtypes = [C.c_void_p, C.c_void_p, C.c_uint8, C.c_void_p]
        return QStatus(self.__lib.alljoyn_authlistener_requestcredentialsresponse(listener, authContext, accept, credentials)) 


    # wrapper for alljoyn_authlistener_verifycredentialsresponse returns QStatus
    def AuthlistenerVerifycredentialsresponse(self, listener, authContext, accept):  # alljoyn_authlistener, void *, QCC_BOOL
        self.__lib.alljoyn_authlistener_verifycredentialsresponse.restype = C.c_uint
        self.__lib.alljoyn_authlistener_verifycredentialsresponse.argtypes = [C.c_void_p, C.c_void_p, C.c_uint8]
        return QStatus(self.__lib.alljoyn_authlistener_verifycredentialsresponse(listener, authContext, accept)) 


    # wrapper for alljoyn_authlistener_destroy returns void
    def AuthlistenerDestroy(self, listener):  # alljoyn_authlistener
        self.__lib.alljoyn_authlistener_destroy.argtypes = [C.c_void_p]
        self.__lib.alljoyn_authlistener_destroy(listener) 


    # wrapper for alljoyn_authlistenerasync_destroy returns void
    def AuthlistenerasyncDestroy(self, listener):  # alljoyn_authlistener
        self.__lib.alljoyn_authlistenerasync_destroy.argtypes = [C.c_void_p]
        self.__lib.alljoyn_authlistenerasync_destroy(listener) 


    # wrapper for alljoyn_credentials_destroy returns void
    def CredentialsDestroy(self, cred):  # alljoyn_credentials
        self.__lib.alljoyn_credentials_destroy.argtypes = [C.c_void_p]
        self.__lib.alljoyn_credentials_destroy(cred) 


    # wrapper for alljoyn_credentials_isset returns QCC_BOOL
    def CredentialsIsset(self, cred, creds):  # const alljoyn_credentials, uint16_t
        self.__lib.alljoyn_credentials_isset.restype = C.c_uint
        self.__lib.alljoyn_credentials_isset.argtypes = [C.c_void_p, C.c_uint16]
        return self.__lib.alljoyn_credentials_isset(cred, creds) 


    # wrapper for alljoyn_credentials_setpassword returns void
    def CredentialsSetpassword(self, cred, pwd):  # alljoyn_credentials, const char *
        self.__lib.alljoyn_credentials_setpassword.argtypes = [C.c_void_p, C.c_char_p]
        self.__lib.alljoyn_credentials_setpassword(cred, pwd) 


    # wrapper for alljoyn_credentials_setusername returns void
    def CredentialsSetusername(self, cred, userName):  # alljoyn_credentials, const char *
        self.__lib.alljoyn_credentials_setusername.argtypes = [C.c_void_p, C.c_char_p]
        self.__lib.alljoyn_credentials_setusername(cred, userName) 


    # wrapper for alljoyn_credentials_setcertchain returns void
    def CredentialsSetcertchain(self, cred, certChain):  # alljoyn_credentials, const char *
        self.__lib.alljoyn_credentials_setcertchain.argtypes = [C.c_void_p, C.c_char_p]
        self.__lib.alljoyn_credentials_setcertchain(cred, certChain) 


    # wrapper for alljoyn_credentials_setprivatekey returns void
    def CredentialsSetprivatekey(self, cred, pk):  # alljoyn_credentials, const char *
        self.__lib.alljoyn_credentials_setprivatekey.argtypes = [C.c_void_p, C.c_char_p]
        self.__lib.alljoyn_credentials_setprivatekey(cred, pk) 


    # wrapper for alljoyn_credentials_setlogonentry returns void
    def CredentialsSetlogonentry(self, cred, logonEntry):  # alljoyn_credentials, const char *
        self.__lib.alljoyn_credentials_setlogonentry.argtypes = [C.c_void_p, C.c_char_p]
        self.__lib.alljoyn_credentials_setlogonentry(cred, logonEntry) 


    # wrapper for alljoyn_credentials_setexpiration returns void
    def CredentialsSetexpiration(self, cred, expiration):  # alljoyn_credentials, uint32_t
        self.__lib.alljoyn_credentials_setexpiration.argtypes = [C.c_void_p, C.uint32_t]
        self.__lib.alljoyn_credentials_setexpiration(cred, expiration) 


    # wrapper for alljoyn_credentials_getpassword returns const char *
    def CredentialsGetpassword(self, cred):  # const alljoyn_credentials
        self.__lib.alljoyn_credentials_getpassword.restype = C.c_char_p
        self.__lib.alljoyn_credentials_getpassword.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_credentials_getpassword(cred) 


    # wrapper for alljoyn_credentials_getusername returns const char *
    def CredentialsGetusername(self, cred):  # const alljoyn_credentials
        self.__lib.alljoyn_credentials_getusername.restype = C.c_char_p
        self.__lib.alljoyn_credentials_getusername.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_credentials_getusername(cred) 


    # wrapper for alljoyn_credentials_getcertchain returns const char *
    def CredentialsGetcertchain(self, cred):  # const alljoyn_credentials
        self.__lib.alljoyn_credentials_getcertchain.restype = C.c_char_p
        self.__lib.alljoyn_credentials_getcertchain.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_credentials_getcertchain(cred) 


    # wrapper for alljoyn_credentials_getprivateKey returns const char *
    def CredentialsGetprivatekey(self, cred):  # const alljoyn_credentials
        self.__lib.alljoyn_credentials_getprivateKey.restype = C.c_char_p
        self.__lib.alljoyn_credentials_getprivateKey.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_credentials_getprivateKey(cred) 


    # wrapper for alljoyn_credentials_getlogonentry returns const char *
    def CredentialsGetlogonentry(self, cred):  # const alljoyn_credentials
        self.__lib.alljoyn_credentials_getlogonentry.restype = C.c_char_p
        self.__lib.alljoyn_credentials_getlogonentry.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_credentials_getlogonentry(cred) 


    # wrapper for alljoyn_credentials_getexpiration returns uint32_t
    def CredentialsGetexpiration(self, cred):  # const alljoyn_credentials
        self.__lib.alljoyn_credentials_getexpiration.restype = C.c_uint32
        self.__lib.alljoyn_credentials_getexpiration.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_credentials_getexpiration(cred) 


    # wrapper for alljoyn_credentials_clear returns void
    def CredentialsClear(self, cred):  # alljoyn_credentials
        self.__lib.alljoyn_credentials_clear.argtypes = [C.c_void_p]
        self.__lib.alljoyn_credentials_clear(cred) 


    # wrapper for alljoyn_pinglistener_destroy returns void
    def PinglistenerDestroy(self, listener):  # alljoyn_pinglistener
        self.__lib.alljoyn_pinglistener_destroy.argtypes = [C.c_void_p]
        self.__lib.alljoyn_pinglistener_destroy(listener) 


    # wrapper for alljoyn_autopinger_create returns alljoyn_autopinger
    def AutopingerCreate(self, bus):  # alljoyn_busattachment
        self.__lib.alljoyn_autopinger_create.restype = C.c_int32
        self.__lib.alljoyn_autopinger_create.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_autopinger_create(bus) 


    # wrapper for alljoyn_autopinger_destroy returns void
    def AutopingerDestroy(self, autopinger):  # alljoyn_autopinger
        self.__lib.alljoyn_autopinger_destroy.argtypes = [C.c_void_p]
        self.__lib.alljoyn_autopinger_destroy(autopinger) 


    # wrapper for alljoyn_autopinger_pause returns void
    def AutopingerPause(self, autopinger):  # alljoyn_autopinger
        self.__lib.alljoyn_autopinger_pause.argtypes = [C.c_void_p]
        self.__lib.alljoyn_autopinger_pause(autopinger) 


    # wrapper for alljoyn_autopinger_resume returns void
    def AutopingerResume(self, autopinger):  # alljoyn_autopinger
        self.__lib.alljoyn_autopinger_resume.argtypes = [C.c_void_p]
        self.__lib.alljoyn_autopinger_resume(autopinger) 


    # wrapper for alljoyn_autopinger_addpinggroup returns void
    def AutopingerAddpinggroup(self, autopinger, group, listener, pinginterval):  # alljoyn_autopinger, const char *, alljoyn_pinglistener, uint32_t
        self.__lib.alljoyn_autopinger_addpinggroup.argtypes = [C.c_void_p, C.c_char_p, C.c_void_p, C.uint32_t]
        self.__lib.alljoyn_autopinger_addpinggroup(autopinger, group, listener, pinginterval) 


    # wrapper for alljoyn_autopinger_removepinggroup returns void
    def AutopingerRemovepinggroup(self, autopinger, group):  # alljoyn_autopinger, const char *
        self.__lib.alljoyn_autopinger_removepinggroup.argtypes = [C.c_void_p, C.c_char_p]
        self.__lib.alljoyn_autopinger_removepinggroup(autopinger, group) 


    # wrapper for alljoyn_autopinger_setpinginterval returns QStatus
    def AutopingerSetpinginterval(self, autopinger, group, pinginterval):  # alljoyn_autopinger, const char *, uint32_t
        self.__lib.alljoyn_autopinger_setpinginterval.restype = C.c_uint
        self.__lib.alljoyn_autopinger_setpinginterval.argtypes = [C.c_void_p, C.c_char_p, C.uint32_t]
        return QStatus(self.__lib.alljoyn_autopinger_setpinginterval(autopinger, group, pinginterval)) 


    # wrapper for alljoyn_autopinger_adddestination returns QStatus
    def AutopingerAdddestination(self, autopinger, group, destination):  # alljoyn_autopinger, const char *, const char *
        self.__lib.alljoyn_autopinger_adddestination.restype = C.c_uint
        self.__lib.alljoyn_autopinger_adddestination.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_autopinger_adddestination(autopinger, group, destination)) 


    # wrapper for alljoyn_autopinger_removedestination returns QStatus
    def AutopingerRemovedestination(self, autopinger, group, destination, removeall):  # alljoyn_autopinger, const char *, const char *, QCC_BOOL
        self.__lib.alljoyn_autopinger_removedestination.restype = C.c_uint
        self.__lib.alljoyn_autopinger_removedestination.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p, C.c_uint8]
        return QStatus(self.__lib.alljoyn_autopinger_removedestination(autopinger, group, destination, removeall)) 





    # wrapper for alljoyn_buslistener_destroy returns void
    def BuslistenerDestroy(self, listener):  # alljoyn_buslistener
        self.__lib.alljoyn_buslistener_destroy.argtypes = [C.c_void_p]
        self.__lib.alljoyn_buslistener_destroy(listener) 


    # wrapper for alljoyn_busobject_destroy returns void
    def BusobjectDestroy(self, bus):  # alljoyn_busobject
        self.__lib.alljoyn_busobject_destroy.argtypes = [C.c_void_p]
        self.__lib.alljoyn_busobject_destroy(bus) 


    # wrapper for alljoyn_busobject_getpath returns const char *
    def BusobjectGetpath(self, bus):  # alljoyn_busobject
        self.__lib.alljoyn_busobject_getpath.restype = C.c_char_p
        self.__lib.alljoyn_busobject_getpath.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_busobject_getpath(bus) 


    # wrapper for alljoyn_busobject_emitpropertychanged returns void
    def BusobjectEmitpropertychanged(self, bus, ifcName, propName, val, id):  # alljoyn_busobject, const char *, const char *, alljoyn_msgarg, alljoyn_sessionid
        self.__lib.alljoyn_busobject_emitpropertychanged.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p, C.c_void_p, C.c_uint32]
        self.__lib.alljoyn_busobject_emitpropertychanged(bus, ifcName, propName, val, id) 


    # wrapper for alljoyn_busobject_emitpropertieschanged returns void
    def BusobjectEmitpropertieschanged(self, bus, ifcName, propNames, numProps, id):  # alljoyn_busobject, const char *, const char * *, size_t, alljoyn_sessionid
        self.__lib.alljoyn_busobject_emitpropertieschanged.argtypes = [C.c_void_p, C.c_char_p, POINTER(C.c_char_p), C.csize_t, C.c_uint32]
        self.__lib.alljoyn_busobject_emitpropertieschanged(bus, ifcName, propNames, numProps, id) 


    # wrapper for alljoyn_busobject_getname returns size_t
    def BusobjectGetname(self, bus, buffer, bufferSz):  # alljoyn_busobject, char *, size_t
        self.__lib.alljoyn_busobject_getname.restype = C.c_size_t
        self.__lib.alljoyn_busobject_getname.argtypes = [C.c_void_p, C.c_char_p, C.csize_t]
        return self.__lib.alljoyn_busobject_getname(bus, buffer, bufferSz) 


    # wrapper for alljoyn_busobject_addinterface returns QStatus
    def BusobjectAddinterface(self, bus, iface):  # alljoyn_busobject, const alljoyn_interfacedescription
        self.__lib.alljoyn_busobject_addinterface.restype = C.c_uint
        self.__lib.alljoyn_busobject_addinterface.argtypes = [C.c_void_p, C.c_void_p]
        return QStatus(self.__lib.alljoyn_busobject_addinterface(bus, iface)) 


    # wrapper for alljoyn_busobject_methodreply_args returns QStatus
    def BusobjectMethodreplyArgs(self, bus, msg, args, numArgs):  # alljoyn_busobject, alljoyn_message, const alljoyn_msgarg, size_t
        self.__lib.alljoyn_busobject_methodreply_args.restype = C.c_uint
        self.__lib.alljoyn_busobject_methodreply_args.argtypes = [C.c_void_p, C.c_void_p, C.c_void_p, C.csize_t]
        return QStatus(self.__lib.alljoyn_busobject_methodreply_args(bus, msg, args, numArgs)) 


    # wrapper for alljoyn_busobject_methodreply_err returns QStatus
    def BusobjectMethodreplyErr(self, bus, msg, error, errorMessage):  # alljoyn_busobject, alljoyn_message, const char *, const char *
        self.__lib.alljoyn_busobject_methodreply_err.restype = C.c_uint
        self.__lib.alljoyn_busobject_methodreply_err.argtypes = [C.c_void_p, C.c_void_p, C.c_char_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_busobject_methodreply_err(bus, msg, error, errorMessage)) 


    # wrapper for alljoyn_busobject_methodreply_status returns QStatus
    def BusobjectMethodreplyStatus(self, bus, msg, status):  # alljoyn_busobject, alljoyn_message, QStatus
        self.__lib.alljoyn_busobject_methodreply_status.restype = C.c_uint
        self.__lib.alljoyn_busobject_methodreply_status.argtypes = [C.c_void_p, C.c_void_p, C.c_uint32]
        return QStatus(self.__lib.alljoyn_busobject_methodreply_status(bus, msg, status)) 


    # wrapper for alljoyn_busobject_getbusattachment returns const alljoyn_busattachment
    def BusobjectGetbusattachment(self, bus):  # alljoyn_busobject
        self.__lib.alljoyn_busobject_getbusattachment.restype = C.c_void_p
        self.__lib.alljoyn_busobject_getbusattachment.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_busobject_getbusattachment(bus) 


    # wrapper for alljoyn_busobject_signal returns QStatus
    def BusobjectSignal(self, bus, destination, sessionId, signal, args, numArgs, timeToLive, flags, msg):  # alljoyn_busobject, const char *, alljoyn_sessionid, const alljoyn_interfacedescription_member, const alljoyn_msgarg, size_t, uint16_t, uint8_t, alljoyn_message
        self.__lib.alljoyn_busobject_signal.restype = C.c_uint
        self.__lib.alljoyn_busobject_signal.argtypes = [C.c_void_p, C.c_char_p, C.c_uint32, C.c_void_p, C.c_void_p, C.csize_t, C.c_uint16, C.c_uint8, C.c_void_p]
        return QStatus(self.__lib.alljoyn_busobject_signal(bus, destination, sessionId, signal, args, numArgs, timeToLive, flags, msg)) 


    # wrapper for alljoyn_busobject_cancelsessionlessmessage_serial returns QStatus
    def BusobjectCancelsessionlessmessageSerial(self, bus, serialNumber):  # alljoyn_busobject, uint32_t
        self.__lib.alljoyn_busobject_cancelsessionlessmessage_serial.restype = C.c_uint
        self.__lib.alljoyn_busobject_cancelsessionlessmessage_serial.argtypes = [C.c_void_p, C.uint32_t]
        return QStatus(self.__lib.alljoyn_busobject_cancelsessionlessmessage_serial(bus, serialNumber)) 


    # wrapper for alljoyn_busobject_issecure returns QCC_BOOL
    def BusobjectIssecure(self, bus):  # alljoyn_busobject
        self.__lib.alljoyn_busobject_issecure.restype = C.c_uint
        self.__lib.alljoyn_busobject_issecure.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_busobject_issecure(bus) 


    # wrapper for alljoyn_busobject_getannouncedinterfacenames returns size_t
    def BusobjectGetannouncedinterfacenames(self, bus, interfaces, numInterfaces):  # alljoyn_busobject, const char * *, size_t
        self.__lib.alljoyn_busobject_getannouncedinterfacenames.restype = C.c_size_t
        self.__lib.alljoyn_busobject_getannouncedinterfacenames.argtypes = [C.c_void_p, POINTER(C.c_char_p), C.csize_t]
        return self.__lib.alljoyn_busobject_getannouncedinterfacenames(bus, interfaces, numInterfaces) 


    # wrapper for alljoyn_busobject_addinterface_announced returns QStatus
    def BusobjectAddinterfaceAnnounced(self, bus, iface):  # alljoyn_busobject, const alljoyn_interfacedescription
        self.__lib.alljoyn_busobject_addinterface_announced.restype = C.c_uint
        self.__lib.alljoyn_busobject_addinterface_announced.argtypes = [C.c_void_p, C.c_void_p]
        return QStatus(self.__lib.alljoyn_busobject_addinterface_announced(bus, iface)) 


    # wrapper for alljoyn_init returns QStatus
    def Init(self):  # void
        self.__lib.alljoyn_init.restype = C.c_uint
        return QStatus(self.__lib.alljoyn_init()) 


    # wrapper for alljoyn_shutdown returns QStatus
    def Shutdown(self):  # void
        self.__lib.alljoyn_shutdown.restype = C.c_uint
        return QStatus(self.__lib.alljoyn_shutdown()) 


    # wrapper for alljoyn_routerinit returns QStatus
    def Routerinit(self):  # void
        self.__lib.alljoyn_routerinit.restype = C.c_uint
        return QStatus(self.__lib.alljoyn_routerinit()) 


    # wrapper for alljoyn_routershutdown returns QStatus
    def Routershutdown(self):  # void
        self.__lib.alljoyn_routershutdown.restype = C.c_uint
        return QStatus(self.__lib.alljoyn_routershutdown()) 

    # wrapper for alljoyn_interfacedescription_activate returns void
    def InterfacedescriptionActivate(self, iface):  # alljoyn_interfacedescription
        self.__lib.alljoyn_interfacedescription_activate.argtypes = [C.c_void_p]
        self.__lib.alljoyn_interfacedescription_activate(iface) 


    # wrapper for alljoyn_interfacedescription_addannotation returns QStatus
    def InterfacedescriptionAddannotation(self, iface, name, value):  # alljoyn_interfacedescription, const char *, const char *
        self.__lib.alljoyn_interfacedescription_addannotation.restype = C.c_uint
        self.__lib.alljoyn_interfacedescription_addannotation.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_interfacedescription_addannotation(iface, name, value)) 


    # wrapper for alljoyn_interfacedescription_getannotation returns QCC_BOOL
    def InterfacedescriptionGetannotation(self, iface, name, value, value_size):  # alljoyn_interfacedescription, const char *, char *, size_t *
        self.__lib.alljoyn_interfacedescription_getannotation.restype = C.c_uint
        self.__lib.alljoyn_interfacedescription_getannotation.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p, POINTER(C.csize_t)]
        return self.__lib.alljoyn_interfacedescription_getannotation(iface, name, value, value_size) 


    # wrapper for alljoyn_interfacedescription_getannotationscount returns size_t
    def InterfacedescriptionGetannotationscount(self, iface):  # alljoyn_interfacedescription
        self.__lib.alljoyn_interfacedescription_getannotationscount.restype = C.c_size_t
        self.__lib.alljoyn_interfacedescription_getannotationscount.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_interfacedescription_getannotationscount(iface) 


    # wrapper for alljoyn_interfacedescription_getannotationatindex returns void
    def InterfacedescriptionGetannotationatindex(self, iface, index, name, name_size, value, value_size):  # alljoyn_interfacedescription, size_t, char *, size_t *, char *, size_t *
        self.__lib.alljoyn_interfacedescription_getannotationatindex.argtypes = [C.c_void_p, C.csize_t, C.c_char_p, POINTER(C.csize_t), C.c_char_p, POINTER(C.csize_t)]
        self.__lib.alljoyn_interfacedescription_getannotationatindex(iface, index, name, name_size, value, value_size) 


    # wrapper for alljoyn_interfacedescription_getmember returns QCC_BOOL
    def InterfacedescriptionGetmember(self, iface, name, member):  # const alljoyn_interfacedescription, const char *, alljoyn_interfacedescription_member *
        self.__lib.alljoyn_interfacedescription_getmember.restype = C.c_uint
        self.__lib.alljoyn_interfacedescription_getmember.argtypes = [C.c_void_p, C.c_char_p, POINTER(C.c_void_p)]
        return self.__lib.alljoyn_interfacedescription_getmember(iface, name, member) 


    # wrapper for alljoyn_interfacedescription_addmemberannotation returns QStatus
    def InterfacedescriptionAddmemberannotation(self, iface, member, name, value):  # alljoyn_interfacedescription, const char *, const char *, const char *
        self.__lib.alljoyn_interfacedescription_addmemberannotation.restype = C.c_uint
        self.__lib.alljoyn_interfacedescription_addmemberannotation.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_interfacedescription_addmemberannotation(iface, member, name, value)) 


    # wrapper for alljoyn_interfacedescription_getmembers returns size_t
    def InterfacedescriptionGetmembers(self, iface, members, numMembers):  # const alljoyn_interfacedescription, alljoyn_interfacedescription_member *, size_t
        self.__lib.alljoyn_interfacedescription_getmembers.restype = C.c_size_t
        self.__lib.alljoyn_interfacedescription_getmembers.argtypes = [C.c_void_p, POINTER(C.c_void_p), C.csize_t]
        return self.__lib.alljoyn_interfacedescription_getmembers(iface, members, numMembers) 


    # wrapper for alljoyn_interfacedescription_hasmember returns QCC_BOOL
    def InterfacedescriptionHasmember(self, iface, name, inSig, outSig):  # alljoyn_interfacedescription, const char *, const char *, const char *
        self.__lib.alljoyn_interfacedescription_hasmember.restype = C.c_uint
        self.__lib.alljoyn_interfacedescription_hasmember.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p, C.c_char_p]
        return self.__lib.alljoyn_interfacedescription_hasmember(iface, name, inSig, outSig) 


    # wrapper for alljoyn_interfacedescription_addmethod returns QStatus
    def InterfacedescriptionAddmethod(self, iface, name, inputSig, outSig, argNames, annotation, accessPerms):  # alljoyn_interfacedescription, const char *, const char *, const char *, const char *, uint8_t, const char *
        self.__lib.alljoyn_interfacedescription_addmethod.restype = C.c_uint
        self.__lib.alljoyn_interfacedescription_addmethod.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p, C.c_char_p, C.c_char_p, C.c_uint8, C.c_char_p]
        return QStatus(self.__lib.alljoyn_interfacedescription_addmethod(iface, name, inputSig, outSig, argNames, annotation, accessPerms)) 


    # wrapper for alljoyn_interfacedescription_getmethod returns QCC_BOOL
    def InterfacedescriptionGetmethod(self, iface, name, member):  # alljoyn_interfacedescription, const char *, alljoyn_interfacedescription_member *
        self.__lib.alljoyn_interfacedescription_getmethod.restype = C.c_uint
        self.__lib.alljoyn_interfacedescription_getmethod.argtypes = [C.c_void_p, C.c_char_p, POINTER(C.c_void_p)]
        return self.__lib.alljoyn_interfacedescription_getmethod(iface, name, member) 


    # wrapper for alljoyn_interfacedescription_addsignal returns QStatus
    def InterfacedescriptionAddsignal(self, iface, name, sig, argNames, annotation, accessPerms):  # alljoyn_interfacedescription, const char *, const char *, const char *, uint8_t, const char *
        self.__lib.alljoyn_interfacedescription_addsignal.restype = C.c_uint
        self.__lib.alljoyn_interfacedescription_addsignal.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p, C.c_char_p, C.c_uint8, C.c_char_p]
        return QStatus(self.__lib.alljoyn_interfacedescription_addsignal(iface, name, sig, argNames, annotation, accessPerms)) 


    # wrapper for alljoyn_interfacedescription_getsignal returns QCC_BOOL
    def InterfacedescriptionGetsignal(self, iface, name, member):  # alljoyn_interfacedescription, const char *, alljoyn_interfacedescription_member *
        self.__lib.alljoyn_interfacedescription_getsignal.restype = C.c_uint
        self.__lib.alljoyn_interfacedescription_getsignal.argtypes = [C.c_void_p, C.c_char_p, POINTER(C.c_void_p)]
        return self.__lib.alljoyn_interfacedescription_getsignal(iface, name, member) 


    # wrapper for alljoyn_interfacedescription_addproperty returns QStatus
    def InterfacedescriptionAddproperty(self, iface, name, signature, access):  # alljoyn_interfacedescription, const char *, const char *, uint8_t
        self.__lib.alljoyn_interfacedescription_addproperty.restype = C.c_uint
        self.__lib.alljoyn_interfacedescription_addproperty.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p, C.c_uint8]
        return QStatus(self.__lib.alljoyn_interfacedescription_addproperty(iface, name, signature, access)) 


    # wrapper for alljoyn_interfacedescription_addpropertyannotation returns QStatus
    def InterfacedescriptionAddpropertyannotation(self, iface, property, name, value):  # alljoyn_interfacedescription, const char *, const char *, const char *
        self.__lib.alljoyn_interfacedescription_addpropertyannotation.restype = C.c_uint
        self.__lib.alljoyn_interfacedescription_addpropertyannotation.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_interfacedescription_addpropertyannotation(iface, property, name, value)) 


    # wrapper for alljoyn_interfacedescription_getpropertyannotation returns QCC_BOOL
    def InterfacedescriptionGetpropertyannotation(self, iface, property, name, value, str_size):  # alljoyn_interfacedescription, const char *, const char *, char *, size_t *
        self.__lib.alljoyn_interfacedescription_getpropertyannotation.restype = C.c_uint
        self.__lib.alljoyn_interfacedescription_getpropertyannotation.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p, C.c_char_p, POINTER(C.csize_t)]
        return self.__lib.alljoyn_interfacedescription_getpropertyannotation(iface, property, name, value, str_size) 


    # wrapper for alljoyn_interfacedescription_hasproperty returns QCC_BOOL
    def InterfacedescriptionHasproperty(self, iface, name):  # const alljoyn_interfacedescription, const char *
        self.__lib.alljoyn_interfacedescription_hasproperty.restype = C.c_uint
        self.__lib.alljoyn_interfacedescription_hasproperty.argtypes = [C.c_void_p, C.c_char_p]
        return self.__lib.alljoyn_interfacedescription_hasproperty(iface, name) 


    # wrapper for alljoyn_interfacedescription_hasproperties returns QCC_BOOL
    def InterfacedescriptionHasproperties(self, iface):  # const alljoyn_interfacedescription
        self.__lib.alljoyn_interfacedescription_hasproperties.restype = C.c_uint
        self.__lib.alljoyn_interfacedescription_hasproperties.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_interfacedescription_hasproperties(iface) 


    # wrapper for alljoyn_interfacedescription_getname returns const char *
    def InterfacedescriptionGetname(self, iface):  # const alljoyn_interfacedescription
        self.__lib.alljoyn_interfacedescription_getname.restype = C.c_char_p
        self.__lib.alljoyn_interfacedescription_getname.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_interfacedescription_getname(iface) 


    # wrapper for alljoyn_interfacedescription_introspect returns size_t
    def InterfacedescriptionIntrospect(self, iface, str, buf, indent):  # const alljoyn_interfacedescription, char *, size_t, size_t
        self.__lib.alljoyn_interfacedescription_introspect.restype = C.c_size_t
        self.__lib.alljoyn_interfacedescription_introspect.argtypes = [C.c_void_p, C.c_char_p, C.csize_t, C.csize_t]
        return self.__lib.alljoyn_interfacedescription_introspect(iface, str, buf, indent) 


    # wrapper for alljoyn_interfacedescription_issecure returns QCC_BOOL
    def InterfacedescriptionIssecure(self, iface):  # const alljoyn_interfacedescription
        self.__lib.alljoyn_interfacedescription_issecure.restype = C.c_uint
        self.__lib.alljoyn_interfacedescription_issecure.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_interfacedescription_issecure(iface) 


    # wrapper for alljoyn_interfacedescription_getsecuritypolicy returns alljoyn_interfacedescription_securitypolicy
    def InterfacedescriptionGetsecuritypolicy(self, iface):  # const alljoyn_interfacedescription
        self.__lib.alljoyn_interfacedescription_getsecuritypolicy.restype = C.c_int32
        self.__lib.alljoyn_interfacedescription_getsecuritypolicy.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_interfacedescription_getsecuritypolicy(iface) 


    # wrapper for alljoyn_interfacedescription_eql returns QCC_BOOL
    def InterfacedescriptionEql(self, one, other):  # const alljoyn_interfacedescription, const alljoyn_interfacedescription
        self.__lib.alljoyn_interfacedescription_eql.restype = C.c_uint
        self.__lib.alljoyn_interfacedescription_eql.argtypes = [C.c_void_p, C.c_void_p]
        return self.__lib.alljoyn_interfacedescription_eql(one, other) 


    # wrapper for alljoyn_interfacedescription_member_eql returns QCC_BOOL
    def InterfacedescriptionMemberEql(self, one, other):  # const alljoyn_interfacedescription_member, const alljoyn_interfacedescription_member
        self.__lib.alljoyn_interfacedescription_member_eql.restype = C.c_uint
        self.__lib.alljoyn_interfacedescription_member_eql.argtypes = [C.c_void_p, C.c_void_p]
        return self.__lib.alljoyn_interfacedescription_member_eql(one, other) 


    # wrapper for alljoyn_keystorelistener_destroy returns void
    def KeystorelistenerDestroy(self, listener):  # alljoyn_keystorelistener
        self.__lib.alljoyn_keystorelistener_destroy.argtypes = [C.c_void_p]
        self.__lib.alljoyn_keystorelistener_destroy(listener) 


    # wrapper for alljoyn_keystorelistener_putkeys returns QStatus
    def KeystorelistenerPutkeys(self, listener, keyStore, source, password):  # alljoyn_keystorelistener, alljoyn_keystore, const char *, const char *
        self.__lib.alljoyn_keystorelistener_putkeys.restype = C.c_uint
        self.__lib.alljoyn_keystorelistener_putkeys.argtypes = [C.c_void_p, C.c_void_p, C.c_char_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_keystorelistener_putkeys(listener, keyStore, source, password)) 


    # wrapper for alljoyn_keystorelistener_getkeys returns QStatus
    def KeystorelistenerGetkeys(self, listener, keyStore, sink, sink_sz):  # alljoyn_keystorelistener, alljoyn_keystore, char *, size_t *
        self.__lib.alljoyn_keystorelistener_getkeys.restype = C.c_uint
        self.__lib.alljoyn_keystorelistener_getkeys.argtypes = [C.c_void_p, C.c_void_p, C.c_char_p, POINTER(C.csize_t)]
        return QStatus(self.__lib.alljoyn_keystorelistener_getkeys(listener, keyStore, sink, sink_sz)) 







    # wrapper for alljoyn_observerlistener_destroy returns void
    def ObserverlistenerDestroy(self, listener):  # alljoyn_observerlistener
        self.__lib.alljoyn_observerlistener_destroy.argtypes = [C.c_void_p]
        self.__lib.alljoyn_observerlistener_destroy(listener) 


    # wrapper for alljoyn_observer_create returns alljoyn_observer
    def ObserverCreate(self, bus, mandatoryInterfaces, numMandatoryInterfaces):  # alljoyn_busattachment, const char *, size_t
        self.__lib.alljoyn_observer_create.restype = C.c_void_p
        self.__lib.alljoyn_observer_create.argtypes = [C.c_void_p, C.c_char_p, C.csize_t]
        return self.__lib.alljoyn_observer_create(bus, mandatoryInterfaces, numMandatoryInterfaces) 


    # wrapper for alljoyn_observer_destroy returns void
    def ObserverDestroy(self, observer):  # alljoyn_observer
        self.__lib.alljoyn_observer_destroy.argtypes = [C.c_void_p]
        self.__lib.alljoyn_observer_destroy(observer) 


    # wrapper for alljoyn_observer_registerlistener returns void
    def ObserverRegisterlistener(self, observer, listener, triggerOnExisting):  # alljoyn_observer, alljoyn_observerlistener, QCC_BOOL
        self.__lib.alljoyn_observer_registerlistener.argtypes = [C.c_void_p, C.c_void_p, C.c_uint8]
        self.__lib.alljoyn_observer_registerlistener(observer, listener, triggerOnExisting) 


    # wrapper for alljoyn_observer_unregisterlistener returns void
    def ObserverUnregisterlistener(self, observer, listener):  # alljoyn_observer, alljoyn_observerlistener
        self.__lib.alljoyn_observer_unregisterlistener.argtypes = [C.c_void_p, C.c_void_p]
        self.__lib.alljoyn_observer_unregisterlistener(observer, listener) 


    # wrapper for alljoyn_observer_unregisteralllisteners returns void
    def ObserverUnregisteralllisteners(self, observer):  # alljoyn_observer
        self.__lib.alljoyn_observer_unregisteralllisteners.argtypes = [C.c_void_p]
        self.__lib.alljoyn_observer_unregisteralllisteners(observer) 


    # wrapper for alljoyn_passwordmanager_setcredentials returns QStatus
    def PasswordmanagerSetcredentials(self, authMechanism, password):  # const char *, const char *
        self.__lib.alljoyn_passwordmanager_setcredentials.restype = C.c_uint
        self.__lib.alljoyn_passwordmanager_setcredentials.argtypes = [C.c_char_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_passwordmanager_setcredentials(authMechanism, password)) 


    # wrapper for alljoyn_proxybusobject_create returns alljoyn_proxybusobject
    def ProxybusobjectCreate(self, bus, service, path, sessionId):  # alljoyn_busattachment, const char *, const char *, alljoyn_sessionid
        self.__lib.alljoyn_proxybusobject_create.restype = C.c_void_p
        self.__lib.alljoyn_proxybusobject_create.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p, C.c_uint32]
        return self.__lib.alljoyn_proxybusobject_create(bus, service, path, sessionId) 


    # wrapper for alljoyn_proxybusobject_create_secure returns alljoyn_proxybusobject
    def ProxybusobjectCreateSecure(self, bus, service, path, sessionId):  # alljoyn_busattachment, const char *, const char *, alljoyn_sessionid
        self.__lib.alljoyn_proxybusobject_create_secure.restype = C.c_void_p
        self.__lib.alljoyn_proxybusobject_create_secure.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p, C.c_uint32]
        return self.__lib.alljoyn_proxybusobject_create_secure(bus, service, path, sessionId) 


    # wrapper for alljoyn_proxybusobject_destroy returns void
    def ProxybusobjectDestroy(self, proxyObj):  # alljoyn_proxybusobject
        self.__lib.alljoyn_proxybusobject_destroy.argtypes = [C.c_void_p]
        self.__lib.alljoyn_proxybusobject_destroy(proxyObj) 


    # wrapper for alljoyn_proxybusobject_addinterface returns QStatus
    def ProxybusobjectAddinterface(self, proxyObj, iface):  # alljoyn_proxybusobject, const alljoyn_interfacedescription
        self.__lib.alljoyn_proxybusobject_addinterface.restype = C.c_uint
        self.__lib.alljoyn_proxybusobject_addinterface.argtypes = [C.c_void_p, C.c_void_p]
        return QStatus(self.__lib.alljoyn_proxybusobject_addinterface(proxyObj, iface)) 


    # wrapper for alljoyn_proxybusobject_addinterface_by_name returns QStatus
    def ProxybusobjectAddinterfaceByName(self, proxyObj, name):  # alljoyn_proxybusobject, const char *
        self.__lib.alljoyn_proxybusobject_addinterface_by_name.restype = C.c_uint
        self.__lib.alljoyn_proxybusobject_addinterface_by_name.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_proxybusobject_addinterface_by_name(proxyObj, name)) 


    # wrapper for alljoyn_proxybusobject_getchild returns alljoyn_proxybusobject
    def ProxybusobjectGetchild(self, proxyObj, path):  # alljoyn_proxybusobject, const char *
        self.__lib.alljoyn_proxybusobject_getchild.restype = C.c_void_p
        self.__lib.alljoyn_proxybusobject_getchild.argtypes = [C.c_void_p, C.c_char_p]
        return self.__lib.alljoyn_proxybusobject_getchild(proxyObj, path) 


    # wrapper for alljoyn_proxybusobject_removechild returns QStatus
    def ProxybusobjectRemovechild(self, proxyObj, path):  # alljoyn_proxybusobject, const char *
        self.__lib.alljoyn_proxybusobject_removechild.restype = C.c_uint
        self.__lib.alljoyn_proxybusobject_removechild.argtypes = [C.c_void_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_proxybusobject_removechild(proxyObj, path)) 


    # wrapper for alljoyn_proxybusobject_introspectremoteobject returns QStatus
    def ProxybusobjectIntrospectremoteobject(self, proxyObj):  # alljoyn_proxybusobject
        self.__lib.alljoyn_proxybusobject_introspectremoteobject.restype = C.c_uint
        self.__lib.alljoyn_proxybusobject_introspectremoteobject.argtypes = [C.c_void_p]
        return QStatus(self.__lib.alljoyn_proxybusobject_introspectremoteobject(proxyObj)) 


    # wrapper for alljoyn_proxybusobject_getproperty returns QStatus
    def ProxybusobjectGetproperty(self, proxyObj, iface, property, value):  # alljoyn_proxybusobject, const char *, const char *, alljoyn_msgarg
        self.__lib.alljoyn_proxybusobject_getproperty.restype = C.c_uint
        self.__lib.alljoyn_proxybusobject_getproperty.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p, C.c_void_p]
        return QStatus(self.__lib.alljoyn_proxybusobject_getproperty(proxyObj, iface, property, value)) 


    # wrapper for alljoyn_proxybusobject_getallproperties returns QStatus
    def ProxybusobjectGetallproperties(self, proxyObj, iface, values):  # alljoyn_proxybusobject, const char *, alljoyn_msgarg
        self.__lib.alljoyn_proxybusobject_getallproperties.restype = C.c_uint
        self.__lib.alljoyn_proxybusobject_getallproperties.argtypes = [C.c_void_p, C.c_char_p, C.c_void_p]
        return QStatus(self.__lib.alljoyn_proxybusobject_getallproperties(proxyObj, iface, values)) 


    # wrapper for alljoyn_proxybusobject_setproperty returns QStatus
    def ProxybusobjectSetproperty(self, proxyObj, iface, property, value):  # alljoyn_proxybusobject, const char *, const char *, alljoyn_msgarg
        self.__lib.alljoyn_proxybusobject_setproperty.restype = C.c_uint
        self.__lib.alljoyn_proxybusobject_setproperty.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p, C.c_void_p]
        return QStatus(self.__lib.alljoyn_proxybusobject_setproperty(proxyObj, iface, property, value)) 


    # wrapper for alljoyn_proxybusobject_methodcall returns QStatus
    def ProxybusobjectMethodcall(self, proxyObj, ifaceName, methodName, args, numArgs, replyMsg, timeout, flags):  # alljoyn_proxybusobject, const char *, const char *, const alljoyn_msgarg, size_t, alljoyn_message, uint32_t, uint8_t
        self.__lib.alljoyn_proxybusobject_methodcall.restype = C.c_uint
        self.__lib.alljoyn_proxybusobject_methodcall.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p, C.c_void_p, C.csize_t, C.c_void_p, C.uint32_t, C.c_uint8]
        return QStatus(self.__lib.alljoyn_proxybusobject_methodcall(proxyObj, ifaceName, methodName, args, numArgs, replyMsg, timeout, flags)) 


    # wrapper for alljoyn_proxybusobject_methodcall_member returns QStatus
    def ProxybusobjectMethodcallMember(self, proxyObj, method, args, numArgs, replyMsg, timeout, flags):  # alljoyn_proxybusobject, const alljoyn_interfacedescription_member, const alljoyn_msgarg, size_t, alljoyn_message, uint32_t, uint8_t
        self.__lib.alljoyn_proxybusobject_methodcall_member.restype = C.c_uint
        self.__lib.alljoyn_proxybusobject_methodcall_member.argtypes = [C.c_void_p, C.c_void_p, C.c_void_p, C.csize_t, C.c_void_p, C.uint32_t, C.c_uint8]
        return QStatus(self.__lib.alljoyn_proxybusobject_methodcall_member(proxyObj, method, args, numArgs, replyMsg, timeout, flags)) 


    # wrapper for alljoyn_proxybusobject_methodcall_noreply returns QStatus
    def ProxybusobjectMethodcallNoreply(self, proxyObj, ifaceName, methodName, args, numArgs, flags):  # alljoyn_proxybusobject, const char *, const char *, const alljoyn_msgarg, size_t, uint8_t
        self.__lib.alljoyn_proxybusobject_methodcall_noreply.restype = C.c_uint
        self.__lib.alljoyn_proxybusobject_methodcall_noreply.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p, C.c_void_p, C.csize_t, C.c_uint8]
        return QStatus(self.__lib.alljoyn_proxybusobject_methodcall_noreply(proxyObj, ifaceName, methodName, args, numArgs, flags)) 


    # wrapper for alljoyn_proxybusobject_methodcall_member_noreply returns QStatus
    def ProxybusobjectMethodcallMemberNoreply(self, proxyObj, method, args, numArgs, flags):  # alljoyn_proxybusobject, const alljoyn_interfacedescription_member, const alljoyn_msgarg, size_t, uint8_t
        self.__lib.alljoyn_proxybusobject_methodcall_member_noreply.restype = C.c_uint
        self.__lib.alljoyn_proxybusobject_methodcall_member_noreply.argtypes = [C.c_void_p, C.c_void_p, C.c_void_p, C.csize_t, C.c_uint8]
        return QStatus(self.__lib.alljoyn_proxybusobject_methodcall_member_noreply(proxyObj, method, args, numArgs, flags)) 


    # wrapper for alljoyn_proxybusobject_parsexml returns QStatus
    def ProxybusobjectParsexml(self, proxyObj, xml, identifier):  # alljoyn_proxybusobject, const char *, const char *
        self.__lib.alljoyn_proxybusobject_parsexml.restype = C.c_uint
        self.__lib.alljoyn_proxybusobject_parsexml.argtypes = [C.c_void_p, C.c_char_p, C.c_char_p]
        return QStatus(self.__lib.alljoyn_proxybusobject_parsexml(proxyObj, xml, identifier)) 


    # wrapper for alljoyn_proxybusobject_secureconnection returns QStatus
    def ProxybusobjectSecureconnection(self, proxyObj, forceAuth):  # alljoyn_proxybusobject, QCC_BOOL
        self.__lib.alljoyn_proxybusobject_secureconnection.restype = C.c_uint
        self.__lib.alljoyn_proxybusobject_secureconnection.argtypes = [C.c_void_p, C.c_uint8]
        return QStatus(self.__lib.alljoyn_proxybusobject_secureconnection(proxyObj, forceAuth)) 


    # wrapper for alljoyn_proxybusobject_secureconnectionasync returns QStatus
    def ProxybusobjectSecureconnectionasync(self, proxyObj, forceAuth):  # alljoyn_proxybusobject, QCC_BOOL
        self.__lib.alljoyn_proxybusobject_secureconnectionasync.restype = C.c_uint
        self.__lib.alljoyn_proxybusobject_secureconnectionasync.argtypes = [C.c_void_p, C.c_uint8]
        return QStatus(self.__lib.alljoyn_proxybusobject_secureconnectionasync(proxyObj, forceAuth)) 


    # wrapper for alljoyn_proxybusobject_getinterface returns const alljoyn_interfacedescription
    def ProxybusobjectGetinterface(self, proxyObj, iface):  # alljoyn_proxybusobject, const char *
        self.__lib.alljoyn_proxybusobject_getinterface.restype = C.c_void_p
        self.__lib.alljoyn_proxybusobject_getinterface.argtypes = [C.c_void_p, C.c_char_p]
        return self.__lib.alljoyn_proxybusobject_getinterface(proxyObj, iface) 


    # wrapper for alljoyn_proxybusobject_getpath returns const char *
    def ProxybusobjectGetpath(self, proxyObj):  # alljoyn_proxybusobject
        self.__lib.alljoyn_proxybusobject_getpath.restype = C.c_char_p
        self.__lib.alljoyn_proxybusobject_getpath.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_proxybusobject_getpath(proxyObj) 


    # wrapper for alljoyn_proxybusobject_getservicename returns const char *
    def ProxybusobjectGetservicename(self, proxyObj):  # alljoyn_proxybusobject
        self.__lib.alljoyn_proxybusobject_getservicename.restype = C.c_char_p
        self.__lib.alljoyn_proxybusobject_getservicename.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_proxybusobject_getservicename(proxyObj) 


    # wrapper for alljoyn_proxybusobject_getuniquename returns const char *
    def ProxybusobjectGetuniquename(self, proxyObj):  # alljoyn_proxybusobject
        self.__lib.alljoyn_proxybusobject_getuniquename.restype = C.c_char_p
        self.__lib.alljoyn_proxybusobject_getuniquename.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_proxybusobject_getuniquename(proxyObj) 


    # wrapper for alljoyn_proxybusobject_getsessionid returns alljoyn_sessionid
    def ProxybusobjectGetsessionid(self, proxyObj):  # alljoyn_proxybusobject
        self.__lib.alljoyn_proxybusobject_getsessionid.restype = C.c_uint32
        self.__lib.alljoyn_proxybusobject_getsessionid.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_proxybusobject_getsessionid(proxyObj) 


    # wrapper for alljoyn_proxybusobject_implementsinterface returns QCC_BOOL
    def ProxybusobjectImplementsinterface(self, proxyObj, iface):  # alljoyn_proxybusobject, const char *
        self.__lib.alljoyn_proxybusobject_implementsinterface.restype = C.c_uint
        self.__lib.alljoyn_proxybusobject_implementsinterface.argtypes = [C.c_void_p, C.c_char_p]
        return self.__lib.alljoyn_proxybusobject_implementsinterface(proxyObj, iface) 


    # wrapper for alljoyn_proxybusobject_isvalid returns QCC_BOOL
    def ProxybusobjectIsvalid(self, proxyObj):  # alljoyn_proxybusobject
        self.__lib.alljoyn_proxybusobject_isvalid.restype = C.c_uint
        self.__lib.alljoyn_proxybusobject_isvalid.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_proxybusobject_isvalid(proxyObj) 


    # wrapper for alljoyn_proxybusobject_issecure returns QCC_BOOL
    def ProxybusobjectIssecure(self, proxyObj):  # alljoyn_proxybusobject
        self.__lib.alljoyn_proxybusobject_issecure.restype = C.c_uint
        self.__lib.alljoyn_proxybusobject_issecure.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_proxybusobject_issecure(proxyObj) 


    # wrapper for alljoyn_proxybusobject_enablepropertycaching returns void
    def ProxybusobjectEnablepropertycaching(self, proxyObj):  # alljoyn_proxybusobject
        self.__lib.alljoyn_proxybusobject_enablepropertycaching.argtypes = [C.c_void_p]
        self.__lib.alljoyn_proxybusobject_enablepropertycaching(proxyObj) 


    # wrapper for alljoyn_sessionopts_create returns alljoyn_sessionopts
    def SessionoptsCreate(self, traffic, isMultipoint, proximity, transports):  # uint8_t, QCC_BOOL, uint8_t, alljoyn_transportmask
        self.__lib.alljoyn_sessionopts_create.restype = C.c_void_p
        self.__lib.alljoyn_sessionopts_create.argtypes = [C.c_uint8, C.c_uint8, C.c_uint8, C.c_void_p]
        return self.__lib.alljoyn_sessionopts_create(traffic, isMultipoint, proximity, transports) 


    # wrapper for alljoyn_sessionopts_destroy returns void
    def SessionoptsDestroy(self, opts):  # alljoyn_sessionopts
        self.__lib.alljoyn_sessionopts_destroy.argtypes = [C.c_void_p]
        self.__lib.alljoyn_sessionopts_destroy(opts) 


    # wrapper for alljoyn_sessionopts_get_traffic returns uint8_t
    def SessionoptsGetTraffic(self, opts):  # const alljoyn_sessionopts
        self.__lib.alljoyn_sessionopts_get_traffic.restype = C.c_uint8
        self.__lib.alljoyn_sessionopts_get_traffic.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_sessionopts_get_traffic(opts) 


    # wrapper for alljoyn_sessionopts_set_traffic returns void
    def SessionoptsSetTraffic(self, opts, traffic):  # alljoyn_sessionopts, uint8_t
        self.__lib.alljoyn_sessionopts_set_traffic.argtypes = [C.c_void_p, C.c_uint8]
        self.__lib.alljoyn_sessionopts_set_traffic(opts, traffic) 


    # wrapper for alljoyn_sessionopts_get_multipoint returns QCC_BOOL
    def SessionoptsGetMultipoint(self, opts):  # const alljoyn_sessionopts
        self.__lib.alljoyn_sessionopts_get_multipoint.restype = C.c_uint
        self.__lib.alljoyn_sessionopts_get_multipoint.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_sessionopts_get_multipoint(opts) 


    # wrapper for alljoyn_sessionopts_set_multipoint returns void
    def SessionoptsSetMultipoint(self, opts, isMultipoint):  # alljoyn_sessionopts, QCC_BOOL
        self.__lib.alljoyn_sessionopts_set_multipoint.argtypes = [C.c_void_p, C.c_uint8]
        self.__lib.alljoyn_sessionopts_set_multipoint(opts, isMultipoint) 


    # wrapper for alljoyn_sessionopts_get_proximity returns uint8_t
    def SessionoptsGetProximity(self, opts):  # const alljoyn_sessionopts
        self.__lib.alljoyn_sessionopts_get_proximity.restype = C.c_uint8
        self.__lib.alljoyn_sessionopts_get_proximity.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_sessionopts_get_proximity(opts) 


    # wrapper for alljoyn_sessionopts_set_proximity returns void
    def SessionoptsSetProximity(self, opts, proximity):  # alljoyn_sessionopts, uint8_t
        self.__lib.alljoyn_sessionopts_set_proximity.argtypes = [C.c_void_p, C.c_uint8]
        self.__lib.alljoyn_sessionopts_set_proximity(opts, proximity) 


    # wrapper for alljoyn_sessionopts_get_transports returns alljoyn_transportmask
    def SessionoptsGetTransports(self, opts):  # const alljoyn_sessionopts
        self.__lib.alljoyn_sessionopts_get_transports.restype = C.c_void_p
        self.__lib.alljoyn_sessionopts_get_transports.argtypes = [C.c_void_p]
        return self.__lib.alljoyn_sessionopts_get_transports(opts) 


    # wrapper for alljoyn_sessionopts_set_transports returns void
    def SessionoptsSetTransports(self, opts, transports):  # alljoyn_sessionopts, alljoyn_transportmask
        self.__lib.alljoyn_sessionopts_set_transports.argtypes = [C.c_void_p, C.c_void_p]
        self.__lib.alljoyn_sessionopts_set_transports(opts, transports) 


    # wrapper for alljoyn_sessionopts_iscompatible returns QCC_BOOL
    def SessionoptsIscompatible(self, one, other):  # const alljoyn_sessionopts, const alljoyn_sessionopts
        self.__lib.alljoyn_sessionopts_iscompatible.restype = C.c_uint
        self.__lib.alljoyn_sessionopts_iscompatible.argtypes = [C.c_void_p, C.c_void_p]
        return self.__lib.alljoyn_sessionopts_iscompatible(one, other) 


    # wrapper for alljoyn_sessionopts_cmp returns int32_t
    def SessionoptsCmp(self, one, other):  # const alljoyn_sessionopts, const alljoyn_sessionopts
        self.__lib.alljoyn_sessionopts_cmp.restype = C.c_int32
        self.__lib.alljoyn_sessionopts_cmp.argtypes = [C.c_void_p, C.c_void_p]
        return self.__lib.alljoyn_sessionopts_cmp(one, other) 


    # wrapper for alljoyn_sessionlistener_destroy returns void
    def SessionlistenerDestroy(self, listener):  # alljoyn_sessionlistener
        self.__lib.alljoyn_sessionlistener_destroy.argtypes = [C.c_void_p]
        self.__lib.alljoyn_sessionlistener_destroy(listener) 


    
