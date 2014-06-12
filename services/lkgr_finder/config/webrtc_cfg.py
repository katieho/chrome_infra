WEBRTC_NORMAL_STEPS = [
    'compile',
    'audio_decoder_unittests',
    'common_audio_unittests',
    'common_video_unittests',
    'libjingle_media_unittest',
    'libjingle_p2p_unittest',
    'libjingle_peerconnection_unittest',
    'libjingle_sound_unittest',
    'libjingle_unittest',
    'modules_tests',
    'modules_unittests',
    'system_wrappers_unittests',
    'test_support_unittests',
    'tools_unittests',
    'video_engine_core_unittests',
    'video_engine_tests',
    'voice_engine_unittests',
]

CONFIG = {
  "project": "webrtc",
  "source_vcs": "svn",
  "source_url": "http://webrtc.googlecode.com/svn/",
  "status_url": "https://webrtc-status.appspot.com",
  "error_recipients": "chrome-troopers+alerts@google.com,"
                      "phoglund@google.com,kjellander@google.com",
  "masters": {
    "client.webrtc": {
      "base_url": "https://build.chromium.org/p/client.webrtc",
      "builders": {
        'Win32 Debug': WEBRTC_NORMAL_STEPS,
        'Win32 Release': WEBRTC_NORMAL_STEPS,
        'Win32 Release [large tests]': [
          'audio_device_tests',
          'video_capture_tests',
          'vie_auto_test',
          'voe_auto_test',
        ],
        'Win64 Debug': WEBRTC_NORMAL_STEPS,
        'Win64 Release': WEBRTC_NORMAL_STEPS,
        'Mac32 Debug': WEBRTC_NORMAL_STEPS,
        'Mac32 Release': WEBRTC_NORMAL_STEPS,
        'Mac32 Release [large tests]': [
          'audio_device_tests',
          'video_capture_tests',
          'vie_auto_test',
          'voe_auto_test',
        ],
        'Mac64 Debug': WEBRTC_NORMAL_STEPS,
        'Mac64 Release': WEBRTC_NORMAL_STEPS,
        'Mac Asan': WEBRTC_NORMAL_STEPS,
        'iOS Debug': ['compile'],
        'iOS Release': ['compile'],
        'Linux32 Debug': WEBRTC_NORMAL_STEPS,
        'Linux32 Release': WEBRTC_NORMAL_STEPS,
        'Linux64 Debug': WEBRTC_NORMAL_STEPS,
        'Linux64 Release': WEBRTC_NORMAL_STEPS,
        'Linux64 Release [large tests]': [
          'audioproc_perf',
          'isac_fixed_perf',
          'libjingle_peerconnection_java_unittest',
          'video_capture_tests',
          'vie_auto_test',
          'voe_auto_test',
        ],
        'Linux Clang': WEBRTC_NORMAL_STEPS,
        'Android': ['compile'],
        'Android (dbg)': ['compile'],
        'Android ARM64 (dbg)': ['compile'],
        'Android Clang (dbg)': ['compile'],
        'Chrome OS': WEBRTC_NORMAL_STEPS,
      },
    },
  },
}
